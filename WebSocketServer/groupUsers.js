const axios = require("axios").default;

const GroupUsersAPI = (payload) => {
  return new Promise((resolve) => {
    resolve(axios.post("http://api:5000/group-users", payload));
  });
};

module.exports = GroupUsersAPI;
