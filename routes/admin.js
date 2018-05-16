var express = require('express');
var router = express.Router();

var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;

var User = require('../models/user');
var Channel = require('../models/channel');

router.post('/all', function(req, res, next){
  if(!req.user || req.user.name !== 'Admin') return res.json({
    error: "Must be admin for post all"
  });
  var server = (req.body.server && req.body.server === 'true');
  var user = server ? 'Dixi' : 'Admin';
  var body = req.body.message;
  Channel.getAllChannels(function(err, channels){
    if (err) console.log(err);
    channels.forEach(function(channel){
      Channel.post(channel, user, body);
    });
  });
  res.json({
    author: user,
    body: body,
    time: Date.now()
  });
});

module.exports = router;
