var express = require('express');
var http = require('http');
var path = require('path');
var mongoose = require('mongoose');
var config = require('./config');

var MongoStore = require('connect-mongo')(express);

;
var mongooseConnection = mongoose.connect(config.db.url, function(err) {
    if (err) {
        console.log('Could not connect to database', config.db.url, ' due to error', err);
        process.exit(1);
    }
});

var app = express();

// Express settings
app.disable('x-powered-by');

// Configuration
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.json());
app.use(express.urlencoded());
app.use(express.methodOverride());
app.use(express.cookieParser(config.secret));

app.use(express.session({
    secret: config.sessionSecret,
    store: new MongoStore({
        collection: "sessions",
        mongoose_connection: mongooseConnection.connections[0]
    }),
    cookie: {
        path: '/',
        httpOnly: true,
        maxAge: 1000 * 60 * 60 * 24 * 30
    }
}));


app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
    app.use(express.errorHandler());
}

require('./helpers')(app);
require('./routes')(app);

// Start server if not invoked by require('./app')
if (require.main === module) {
    http.createServer(app).listen(config.port, config.address, function() {
        console.log("Express server listening on %s:%d in %s mode", config.address, config.port, app.settings.env);
    });    
} else {
    // Export app if invoked by require('./app')
    module.exports = app;
}
