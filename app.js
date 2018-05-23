var createError = require('http-errors');
var express = require('express');
var path = require('path');
var formParser = require('express-form-data');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var os = require('os');

var mongoose = require('mongoose');

var session = require('cookie-session');
var passport = require('passport');

var schedule = require('node-schedule');
var jobs = require('./jobs');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var channelsRouter= require('./routes/channels');
var adminRouter = require('./routes/admin');

var app = express();


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(session({
  name: 'session',
  secret: 'session-secret-key',
  resave: false,
  saveUninitialized: true,
}));

app.use(formParser.parse({uploadDir: os.tmpdir(), autoClean: true}));
app.use(formParser.format());
app.use(formParser.stream());
app.use(formParser.union());

app.use(passport.initialize());
app.use(passport.session());

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/channels', channelsRouter);
app.use('/admin', adminRouter);

var j = schedule.scheduleJob('0 3 * * *', function(){
  jobs.prune();
});

app.use(function(req, res, next) {
  next(createError(404));
});

app.use(function(err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  res.status(err.status || 500);
  res.json({error: err.status || 500, message: err.message})
});

var mongoDB = 'mongodb://localhost/dixi';
mongoose.connect(mongoDB);
mongoose.Promise = global.Promise;
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));


module.exports = app;
