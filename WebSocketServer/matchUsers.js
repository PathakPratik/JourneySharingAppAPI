const axios = require("axios").default;

const MatchUsersAPI = async (payload) => {
  try {
    const res = await axios.post("http://api:5000/match-users", payload);
    return res.data;
  } catch (err) {
    return err;
  }
};

module.exports = MatchUsersAPI;
