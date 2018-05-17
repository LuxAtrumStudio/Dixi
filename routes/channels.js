var express = require('express');
var router = express.Router();

var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;

var User = require('../models/user');
var Channel = require('../models/channel');

router.get('/list', function(req, res, next) {
  if (!req.user) return res.json({
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
  var users = req.body.users.split(',');
  var open = req.body.open;
  if (!title) {
    res.json({
      error: "Name is required"
    });
  } else {
    if (!users || users[0] === '') {
      open = true;
      users = [req.user.name];
    } else if (!users.includes(req.user.name)) users.push(req.user.name);
    var newChannel = new Channel({
      title: title,
      users: users,
      open: open,
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
          users: users,
          open: open
        });
      }
    });
  }
});

router.post('/delete', function(req, res, next) {
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  var title = req.body.title;
  Channel.getChannelByName(title, function(err, channel) {
    if (err) console.log(err);
    if (!channel) {
      res.json({
        error: 'channel not found'
      });
    } else if (channel.users.includes(req.user.name)) {
      Channel.deleteChannel(title, function(err) {
        if (err) console.log(err);
        res.json({
          success: true,
          title: title
        });
      });
    } else {
      res.json({
        error: 'Channel not found'
      });
    }
  });
});

module.exports = router;
