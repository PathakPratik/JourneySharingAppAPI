const app = require("express")();
const http = require("http").Server(app);
const io = require("socket.io")(http);
const path = require("path");
const HelloWorld = require("./helloWorld");
const MatchUsers = require("./matchUsers");
const GroupUsers = require("./groupUsers");
const GroupSubscription = require("./GroupSubscription");
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

redis
  .smembers("sub-clients")
  .then((clients) => {
    for (const each of clients) {
      redis.del("sub-" + each).catch((err) => console.log(err));
    }

    redis
      .del("sub-clients")
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
        io.to(clients[i]).emit("routeMatches", {
          action: "routeMatches",
          status,
          data,
        });
      } else {
        const { status, data } = result.reason.response;
        io.to(clients[i]).emit("routeMatches", {
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

// Get list of promises for all active subscription clients
const getActiveSubClientAPIs = (clients) =>
  new Promise(async (resolve) => {
    const promises = [];

    for (const each of clients) {
      const eachPayload = await redis.get("sub-" + each);
      const p = GroupSubscription(JSON.parse(eachPayload));
      promises.push(p);
    }

    resolve(promises);
  });

const broadcastSubscriptions = async (socket) => {
  try {
    const clients = await redis.smembers("sub-clients");
    const promises = await getActiveSubClientAPIs(clients);
    const results = await Promise.allSettled(promises);
    results.forEach((result, i) => {
      if (result.status == "fulfilled") {
        const { status, data } = result.value;
        io.to(clients[i]).emit("groupSubscription", {
          action: "groupSubscription",
          status,
          data,
        });
      } else {
        const { status, data } = result.reason.response;
        io.to(clients[i]).emit("groupSubscription", {
          action: "groupSubscription",
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
  // Connection message
  io.to(socket.id).emit("connected", { action: "connected" });

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
        io.to(socket.id).emit("groupUsers", {
          action: "groupUsers",
          status,
          data,
        });
        await broadcastChanges(socket);
        await broadcastSubscriptions(socket);
      })
      .catch((err) => {
        if (err.hasOwnProperty("response")) {
          const { status, data } = err.response;
          io.to(socket.id).emit("groupUsers", {
            action: "groupUsers",
            status,
            data,
          });
        }
      });
  });

  // Group Subscription
  socket.on("groupSubscription", (payload) => {
    GroupSubscription(payload)
      .then(async (result) => {
        const { status, data } = result;

        // Save every client request
        await redis.sadd("sub-clients", socket.id);
        await redis.set("sub-" + socket.id, JSON.stringify(payload));

        io.to(socket.id).emit("groupSubscription", {
          action: "groupSubscription",
          status,
          data,
        });
      })
      .catch((err) => {
        if (err.hasOwnProperty("response")) {
          const { status, data } = err.response;
          io.to(socket.id).emit("groupSubscription", {
            action: "groupSubscription",
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
