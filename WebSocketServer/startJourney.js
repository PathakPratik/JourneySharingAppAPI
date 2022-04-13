const axios = require("axios").default;

const StartJourneyAPI = (payload) => {
  return new Promise((resolve) => {
    resolve(
      axios.post("http://api:5000/start-journey", JSON.stringify(payload), {
        headers: {
          "Content-Type": "application/json",
        },
      })
    );
  });
};

module.exports = StartJourneyAPI;
