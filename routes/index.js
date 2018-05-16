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
  response = {
    'users': []
  }
  Channel.getChannels(req.user.name, function(err, channels) {
    if (err) console.log(err);
    channels.forEach(function(channel) {
      response.users = response.users.concat(channel.users);
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
    response.users = response.users.filter(function(item, pos) {
      return response.users.indexOf(item) == pos
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
  response = {
    'users': []
  }
  Channel.getChannels(req.user.name, function(err, channels) {
    if (err) console.log(err);
    channels.forEach(function(channel) {
      response.users = response.users.concat(channel.users)
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
    response.users = response.users.filter(function(item, pos) {
      return response.users.indexOf(item) == pos
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
      author: req.user.name,
      body: req.body.message,
      time: Date.now()
    });
  });
});

router.post('/:channel/post', function(req, res, next) {
  if (!req.user) return res.json({
    error: "must be logged in for channels"
  });
  Channel.channelExists(req.params.channel, function(err, result) {
    if (err) console.log(err);
    if (result) {
      Channel.getChannelByName(req.params.channel, function(err, channel) {
        if (err) console.log(err);
        if (channel.users.includes(req.user.name) || channel.open === true) {
          Channel.post(channel, req.user.name, req.body.message);
          res.json({
            author: req.user.name,
            body: req.body.message,
            time: Date.now()
          });
        } else {
          res.json({
            error: "channel not found",
            channel: req.params.channel
          });
        }
      });
    } else {
      res.json({
        error: "channel not found",
        channel: req.params.channel
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
          users: channel.users,
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
