var express = require('express');
var router = express.Router();

var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;

var User = require('../models/user');
var Channel = require('../models/channel');

router.get('/list', function(req, res, next) {
  if (!req.user) res.json({
    error: "must be logged in for channels"
  });
  Channel.getChannels(req.user.name, function(err, results) {
    if (err) console.log(err);
    res.json({
      channels: results.map(x => x.title)
    });
  });
});

router.post('/create', function(req, res, next) {
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  var title = req.body.title;
  var users = req.body.users;
  if (!title) {
    res.json({
      error: "Name is required"
    });
  } else {
    if (!users) users = [req.user.name];
    else if (!users.includes(req.user.name)) users.push(req.user.name);
    var newChannel = new Channel({
      title: title,
      users: users,
      messages: []
    });
    Channel.channelExists(title, function(err, result) {
      if (err) console.log(err);
      if (result) {
        res.json({
          error: "Channel already exists"
        });
      } else {
        Channel.createChannel(newChannel, function(err, result) {
          if (err) throw err;
        });
        res.json({
          success: true,
          title: title,
          users: users
        });
      }
    });
  }
});

module.exports = router;
