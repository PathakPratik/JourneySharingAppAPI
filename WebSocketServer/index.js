const app = require("express")();
const http = require("http").Server(app);
const io = require("socket.io")(http);
const path = require("path");
const HelloWorld = require("./helloWorld");
const MatchUsers = require("./matchUsers");
const Redis = require("ioredis");

const redis = new Redis(6379, "redis");

app.use("/", HelloWorld);

app.get("/", function (req, res) {
  res.sendFile(path.resolve(__dirname, "./index.html"));
});

redis
  .del("clients")
  .then((res) => console.log("Restarted Socket Server:", res))
  .catch((err) => console.log(err));

io.on("connection", async (socket) => {
  await redis.sadd("clients", socket.id);

  socket.on("routeMatches", async (payload) => {
    try {
      const res = await MatchUsers(payload);
      msg = {
        action: "routeMatches",
        res,
      };
      io.to(socket.id).emit("routeMatchesResponse", msg);
    } catch (err) {
      console.log("Something went wrong!!");
    }
  });

  socket.on("disconnect", async () => {
    await redis.srem("clients", socket.id);
  });
});

http.listen(3000, function () {
  console.log("listening on *:3000");
});
