const axios = require("axios").default;

const GroupSubscriptionAPI = (payload) => {
  return new Promise((resolve) => {
    resolve(
      axios.post(
        "http://api:5000/group-subscription",
        JSON.stringify(payload),
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
    );
  });
};

module.exports = GroupSubscriptionAPI;
