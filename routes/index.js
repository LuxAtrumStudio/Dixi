var express = require('express');
var router = express.Router();

var Channel = require('../models/channel');

/* GET home page. */
router.get('/', function(req, res, next) {
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  var updated = new Date();
  if (req.query.update) {
    updated.setTime(req.query.update);
  } else {
    updated.setDate(updated.getDate() - 14);
  }
  updated = updated.getTime();
  response = {}
  Channel.getChannels(req.user.name, function(err, channels) {
    if (err) console.log(err);
    channels.forEach(function(channel) {
      var title = channel.title;
      response[title] = [];
      for (var i = channel.messages.length - 1; i >= 0; --i) {
        var msg = channel.messages[i];
        var msgDate = new Date(msg.date).getTime();
        if (msgDate <= updated) {
          break;
        }
        response[title].unshift({
          author: msg.author,
          body: msg.body,
          time: msg.date.getTime()
        });
      }
    });
    response.update = Date.now();
    res.json(response);
  });
});

router.get('/update', function(req, res, next) {
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  var updated = new Date();
  if (req.query.update) {
    updated.setTime(req.query.update);
  } else {
    updated.setDate(updated.getDate() - 14);
  }
  updated = updated.getTime();
  response = {}
  Channel.getChannels(req.user.name, function(err, channels) {
    if (err) console.log(err);
    channels.forEach(function(channel) {
      var title = channel.title;
      response[title] = [];
      for (var i = channel.messages.length - 1; i >= 0; --i) {
        var msg = channel.messages[i];
        var msgDate = new Date(msg.date).getTime();
        if (msgDate <= updated) {
          break;
        }
        response[title].unshift({
          author: msg.author,
          body: msg.body,
          time: msg.date.getTime()
        });
      }
    });
    response.update = Date.now();
    res.json(response);
  });
});

router.post('/post', function(req, res, next) {
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
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  console.log(req.params.channel);
  Channel.getChannelByName(req.params.channel, function(err, channel) {
    if (err) console.log(err);
    console.log("FOUND");
    if (channel.users.includes(req.user.name)) {
      console.log("IN");
      Channel.post(channel, req.user.name, req.body.message);
      res.json({
        channel: channel.name,
        user: req.user.name,
        post: req.body.message
      });
    } else {
      res.json({
        error: "channel not found"
      });
    }
  });
});

router.get('/:channel/delete', function(req, res, next) {
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  Channel.getChannelByName(req.params.channel, function(err, channel) {
    if (err) console.log(err);
    if (channel.users.includes(req.user.name)) {
      Channel.deleteChannel(channel.id, function(err, channel){
        if(err) console.log(err);
        res.json({
          message: "deleted channel",
          channel: channel.title
        });
      });
    } else {
      res.json({
        error: "channel not found"
      });
    }
  });
});

router.get('/:channel', function(req, res, next) {
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  Channel.channelExists(req.params.channel, function(err, result) {
    if (err) console.log(err);
    if (result) {
      Channel.getChannelByName(req.params.channel, function(err, channel) {
        if (err) console.log(err);
        if (!req.session.channel || req.session.channel !== channel.id) {
          if (channel.users.includes(req.user.name)) {
            req.session.channel = channel.id;
          } else {}
        }
        var updated = new Date();
        if (req.query.update) {
          updated.setTime(req.query.update);
        } else {
          updated.setDate(updated.getDate() - 14);
        }
        updated = updated.getTime();
        var messages = [];
        for (var i = channel.messages.length - 1; i >= 0; --i) {
          var msg = channel.messages[i];
          var msgDate = new Date(msg.date).getTime();
          if (msgDate <= updated) {
            break;
          }
          messages.unshift({
            author: msg.author,
            body: msg.body,
            time: msg.date.getTime()
          });
        }
        res.json({
          time: Date.now(),
          messages: messages
        });
      });
    } else {
      res.json({
        error: "channel not found"
      });
    }
  });
});

module.exports = router;
