var express = require('express');
var router = express.Router();

var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;

var User = require('../models/user');

passport.use(new LocalStrategy(
  function(username, password, done) {
    User.getUserByName(username, function(err, user) {
      if (err) throw err;
      if (!user) {
        return done(null, false, {
          message: "incorrect username or password"
        });
      }
      User.comparePassword(password, user.password, function(err, isMatch) {
        if (err) throw err;
        if (isMatch) {
          return done(null, user);
        } else {
          return done(null, false, {
            message: "incorrect username or password"
          });
        }
      });
    });
  }
));

passport.serializeUser(function(user, done) {
  done(null, user.id);
});

passport.deserializeUser(function(id, done) {
  User.getUserById(id, function(err, user) {
    done(err, user);
  });
});

router.get('/list', function(req, res, next) {
  User.getUsers(function(err, results) {
    if (err) console.log(err);
    if (req.user) {
      res.json({
        current: req.user.name,
        users: results.map(x => x.name)
      });
    } else {
      res.json({
        users: results.map(x => x.name)
      });
    }
  });
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
      if (err) console.log(err);
      if (result) res.json({
        error: "User already exists"
      });
      else {
        User.createUser(newUser, function(err, result) {
          if (err) throw err;
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

router.post('/login', passport.authenticate('local'), function(req, res, next) {
  res.json({
    success: true,
    name: req.user.name
  });
});

router.get('/current', function(req, res, next) {
  var login = req.user ? true : false;
  if (req.user) {
    res.json({
      loggedin: login,
      name: req.user.name
    });
  } else {
    res.json({
      loggedin: login
    });
  }
});

router.get('/logout', function(req, res, next) {
  req.logout();
  req.session.channel = null;
  res.json({
    loggedout: true
  });
});


module.exports = router;
