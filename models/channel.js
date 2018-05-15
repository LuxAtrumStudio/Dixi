var mongoose = require('mongoose');

var User = require('./user');

var MessageSchema = mongoose.Schema({
  author: String,
  body: String,
  date: { type: Date, default: Date.now }
});

var ChannelSchema = mongoose.Schema({
  title: String,
  users: [String],
  messages: [MessageSchema]
});

var Channel = module.exports = mongoose.model('Channel', ChannelSchema);
var Message = module.exports = mongoose.model('Message', MessageSchema);

module.exports.channelExists = function(channelName, done){
  Channel.findOne({title: channelName}, function(err, result){
    if(err) done(err);
    if(result) done(null, true);
    else done(null, false);
  });
}

module.exports.createChannel = function(newChannel, done){
  newChannel.users.push('Admin');
  newChannel.save(done);
}

module.exports.getChannelByName = function(channelName, done){
  Channel.findOne({title: channelName}, done);
}

module.exports.getChannelById = function(channelId, done){
  Channel.findById(channelId, done);
}

module.exports.userInChannel = function(channelName, userName, callback){
  Channel.findOne({title: channelName}, function(err, channel){
    if (err) callback(err);
    if (!channel) callback(null, false);
    else if (channel.users.includes(userName)) callback(null, true);
    else callback (null, false);
  });
}

module.exports.getChannels = function(userName, callback){
  Channel.find({}, function(err, channels){
    if(err) callback(err);
    var userChannels = [];
    channels.forEach(function(item){
      if (item.users.includes(userName)) userChannels.push(item);
    });
    callback(null, userChannels);
  });
}

module.exports.post = function(channel, author, body){
  var message = new Message({
    author: author,
    body: body
  });
  console.log(channel, author, body);
  channel.messages.push(message);
  channel.save();
}
