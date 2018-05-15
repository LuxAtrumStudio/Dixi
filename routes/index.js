var express = require('express');
var router = express.Router();

var Channel = require('../models/channel');

/* GET home page. */
router.get('/', function(req, res, next) {
  var key = req.param('key');
  console.log(key);
  res.render('index', {
    title: 'Express'
  });
});

router.post('/post', function(req, res, next) {
  console.log(req.session);
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  if (!req.session.channel) return res.json({
    error: "must be connected to a channel to post"
  });
  Channel.getChannelById(req.session.channel, function(err, channel) {
    if (err) console.log(err);
    Channel.post(channel, req.user.name, req.body.message);
    res.json({
      channel: channel.name,
      user: req.user.name,
      post: req.body.message
    });
  });
});

router.post('/:channel/post', function(req, res, next) {
  console.log(req.session);
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  if (!req.session.channel) return res.json({
    error: "must be connected to a channel to post"
  });
  Channel.getChannelById(req.session.channel, function(err, channel) {
    if (err) console.log(err);
    Channel.post(channel, req.user.name, req.body.message);
    res.json({
      channel: channel.name,
      user: req.user.name,
      post: req.body.message
    });
  });
});

router.get('/:channel', function(req, res, next) {
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  Channel.channelExists(req.params.channel, function(err, result) {
    if (err) console.log(err);
    if (result) {
      Channel.userInChannel(req.params.channel, req.user.name, function(err, result) {
        if (err) console.log(err);
        if (result) {
          Channel.getChannelByName(req.params.channel, function(err, result) {
            if (err) console.log(err);
            req.session.channel = result.id;
            req.session.save(function(err) {
              if (err) console.log(err);
            })
          });
          res.json({
            success: true,
            message: "Connected to channel",
            channel: req.params.channel
          });
        } else {
          res.json({
            error: "Current user does not have access to channel",
            channel: req.params.channel,
            user: req.user.name
          });
        }
      });
    } else {
      res.json({
        error: "channel not found"
      });
    }
  });
});

module.exports = router;
