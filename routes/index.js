var express = require('express');
var router = express.Router();

var channel = require('../models/channel.js');

/* GET home page. */
router.get('/', function(req, res, next) {
  var key = req.param('key');
  console.log(key);
  res.render('index', { title: 'Express' });
});

router.get('/channels/create', function(req, res, next){
  var name = req.param('name');
  var users = req.param('users');
  if(!name){
    res.json({error: "No name for channel"});
  }
  if(users){
    users = users.split(',');
  }
  res.json({'name': name, 'users': users});
  channel.create(users, name, function(err, id){
    if(err) console.log(err);
  });
})

module.exports = router;
