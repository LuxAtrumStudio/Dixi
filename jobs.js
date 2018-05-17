var Channel = require('./models/channel');

module.exports.prune = function() {
  if (!String.prototype.format) {
    String.prototype.format = function() {
      var args = arguments;
      return this.replace(/{(\d+)}/g, function(match, number) {
        return typeof args[number] != 'undefined' ?
          args[number] :
          match;
      });
    };
  }
  Channel.getAllChannels(function(err, channels) {
    if (err) console.log(err);
    var cutoff = new Date().setDate(new Date().getDate() - 30);
    for (var i = 0; i < channels.length; i++) {
      if (channels[i].message[-1].body === "{0} will be closed in 24 hours".format(channels[i].title) && channels[i].message[-1].author === "Dixi") {
        Channel.deleteChannel(channels[i].title);
      } else if (new Date(channels[i].messages[-1].date).getTime() <= cutoff) {
        Channel.post(channels[i], 'Dixi', "{0} will be closed in 24 hours".format(channels[i].title));
      }
    }
  });
}
