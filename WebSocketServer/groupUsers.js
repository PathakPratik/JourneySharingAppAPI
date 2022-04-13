const axios = require("axios").default;

const GroupUsersAPI = (payload) => {
  return new Promise((resolve) => {
    resolve(
      axios.post("http://api:5000/group-users", JSON.stringify(payload), {
        headers: {
          "Content-Type": "application/json",
        },
      })
    );
  });
};

module.exports = GroupUsersAPI;
