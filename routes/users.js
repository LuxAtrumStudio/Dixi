var express = require('express');
var router = express.Router();

var User = require('../models/user');

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

router.post('/register', function(req, res, next) {
  var name = req.body.name;
  var email = req.body.email;
  var paswd = req.body.password;
  var paswd2 = req.body.password2;
  if (!name) {
    res.json({
      error: "Name is required"
    });
  } else if (!email) {
    res.json({
      error: "Email is required"
    });
  } else if (!paswd) {
    res.json({
      error: "Password is required"
    });
  } else if (!paswd2) {
    res.json({
      error: "Password confirmation is required"
    });
  } else if (paswd !== paswd2) {
    res.json({
      error: "Passwords must match"
    });
  } else {
    var newUser = new User({
      name: name,
      email: email,
      password: paswd
    });
    User.userExists(newUser, function(err, result) {
      if(err) console.log(err);
      if (result) res.json({
        error: "User already exists"
      });
      else {
        User.createUser(newUser, function(err, result) {
          if (err) throw err;
          console.log(result);
        });
        res.json({
          success: true,
          name: name,
          email: email
        });
      }
    });
  }
});

module.exports = router;
