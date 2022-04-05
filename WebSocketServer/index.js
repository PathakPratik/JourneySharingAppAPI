const app = require("express")();
const http = require("http").Server(app);
const io = require("socket.io")(http);
const path = require("path");
const HelloWorld = require("./helloWorld");
const MatchUsers = require("./matchUsers");
const GroupUsers = require("./groupUsers");
const Redis = require("ioredis");

const redis = new Redis(6379, "redis");

app.use("/", HelloWorld);

app.get("/", function (req, res) {
  res.sendFile(path.resolve(__dirname, "./index.html"));
});

// Flush the clients from DB during server restart
redis
  .smembers("clients")
  .then((clients) => {
    for (const each of clients) {
      redis.del(each).catch((err) => console.log(err));
    }

    redis
      .del("clients")
      .then((res) => console.log("Restarted Socket Server:", res))
      .catch((err) => console.log(err));
  })
  .catch((err) => console.log(err));

// Get list of promises for all active clients match results
const getActiveClientAPIs = (clients) =>
  new Promise(async (resolve) => {
    const promises = [];

    for (const each of clients) {
      const eachPayload = await redis.get(each);
      const p = MatchUsers(JSON.parse(eachPayload));
      promises.push(p);
    }

    resolve(promises);
  });

// Broadcast DB changes to all active clients
const broadcastChanges = async (socket) => {
  try {
    const clients = await redis.smembers("clients");
    const promises = await getActiveClientAPIs(clients);
    const results = await Promise.allSettled(promises);
    results.forEach((result, i) => {
      if (result.status == "fulfilled") {
        const { status, data } = result.value;
        io.to(clients[i]).emit({
          action: "routeMatches",
          status,
          data,
        });
      } else {
        const { status, data } = result.reason.response;
        io.to(clients[i]).emit({
          action: "routeMatches",
          status,
          data,
        });
      }
    });
  } catch (err) {
    console.log(err);
    io.to(socket.id).emit({ status: "500", data: err });
  }
};

// Handle Clients
io.on("connection", async (socket) => {
  // routeMatches
  socket.on("routeMatches", async (payload) => {
    // Save every client request
    await redis.sadd("clients", socket.id);
    await redis.set(socket.id, JSON.stringify(payload));
    await broadcastChanges(socket);
  });

  // Group matching users
  socket.on("groupUsers", (payload) => {
    GroupUsers(payload)
      .then(async (result) => {
        const { status, data } = result;
        io.to(socket.id).emit({
          action: "groupUsers",
          status,
          data,
        });
        await broadcastChanges(socket);
      })
      .catch((err) => {
        if (err.hasOwnProperty("response")) {
          const { status, data } = err.response;
          io.to(socket.id).emit({
            action: "groupUsers",
            status,
            data,
          });
        }
      });
  });

  socket.on("disconnect", async () => {
    await redis.srem("clients", socket.id);
  });
});

http.listen(3000, function () {
  console.log("listening on *:3000");
});
