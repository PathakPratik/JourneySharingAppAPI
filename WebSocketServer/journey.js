const axios = require("axios").default;

const JourneyAPI = (payload) => {
  return new Promise((resolve) => {
    resolve(
      axios.post("http://api:5000/journey-action", JSON.stringify(payload), {
        headers: {
          "Content-Type": "application/json",
        },
      })
    );
  });
};

module.exports = JourneyAPI;
