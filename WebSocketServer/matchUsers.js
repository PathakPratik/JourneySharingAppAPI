const express = require('express')
const router = express.Router()
const axios = require('axios').default;

router.get('/hello-world', function(req, res) {
    axios.get('http://api:5000/hello-world')
   .then(function (response) {
     // handle success
     res.json(response.data.message)
   })
   .catch(function (error) {
     // handle error
     res.json(error)
   })
 });

module.exports = router