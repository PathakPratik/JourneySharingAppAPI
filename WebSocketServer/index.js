const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const path = require("path");
const MatchUsers = require("./matchUsers")

app.use('/', MatchUsers)

app.get('/', function(req, res) {
   res.sendFile(path.resolve(__dirname,'./index.html'));
});

io.on('connection', function(socket) {
   console.log('A user connected:', socket.id);

   socket.emit("hello", "world");

   socket.on('disconnect', function () {
      console.log('A user disconnected:', socket.id);
   });
});

http.listen(3000, function() {
   console.log('listening on *:3000');
});