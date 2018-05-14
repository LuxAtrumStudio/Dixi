var db = require('../db.js');

exports.create = function(userIds, text, done) {
  var values = [userIds, text, new Date().toISOString()];

  db.get().query('INSERT INTO channels (users, text, date) Values(?, ?, ?)', values, function(err, result){
    if(err) return done(err);
    done(null, result.insertId);
  });
}

exports.getAll = function(done){
  db.get().query('SELECT * FROM channels', function(err, rows) {
    if(err) return done(err);
    done(null, rows);
  });
}

exports.getAllByUser = function(userIds, done){
  db.get().query('SELECT * FROM channels WHERE user_id = ?', userIds, function(err, rows){
    if(err) return done(err);
    done(null, rows);
  });
}
