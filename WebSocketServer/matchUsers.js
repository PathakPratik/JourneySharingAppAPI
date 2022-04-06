const axios = require("axios").default;

const MatchUsersAPI = (payload) => {
  return new Promise((resolve) => {
    resolve(axios.post("http://api:5000/match-users", payload));
  });
};

module.exports = MatchUsersAPI;
