var mongoose = require('mongoose');
var bcrypt = require('bcryptjs');

var UserSchema = mongoose.Schema({
  name: {
    type: String,
    index: true
  },
  email: {
    type: String
  },
  password: {
    type: String
  },
});

var User = module.exports = mongoose.model('User', UserSchema);

module.exports.userExists = function(newUser, done){
  User.findOne({name: newUser.name}, function(err, result){
    if(err) done(err);
    if(result) done(null, true);
    else done(null, false);
  });
}

module.exports.createUser = function(newUser, done){
  bcrypt.genSalt(10, function(err, salt){
    bcrypt.hash(newUser.password, salt, function(err, hash){
      newUser.password = hash;
      newUser.save(done);
    });
  });
}

module.exports.getUserByUsername = function(username, callback){
  var query = {name: username};
  console.log(query);
  User.findOne(query, callback);
}

module.exports.comparePassword = function(paswd, hash, callback){
  bcrypt.compare(paswd, hash, function(err, isMatch){
    if(err) throw err;
    callback(null, isMatch);
  });
}
