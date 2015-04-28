var User = require('../models/user');
var path = require('path'),
    fs = require('fs');

var allMacs = "No Registered Users"    
var currentTemp = "0";
var currentHumid = "0";
var appStates = [false,false,false,false];
var mainRoutes = [];
var acTemp = 0;
var nop = 0;
function toBool(string)
{
    if(string=="True" || string =="true") return true;
    return false;
}

var requireRoutes = function(dir, app) {
    var files = fs.readdirSync(dir).filter(function(file) {
        return path.join(__dirname, file) != __filename;
    });

    files.forEach(function(file) {
        var absolutePath = path.join(dir, file);
        var stat = fs.statSync(absolutePath);
        if (stat.isFile()) {
            try {
                var defineRoutes = require(absolutePath);
                defineRoutes(app);

                if (defineRoutes.meta) {
                    mainRoutes.push(defineRoutes.meta);
                }
            } catch (e) {
                console.log('Could not require route "' + absolutePath + '" due to exception', e);
            }
        } else if (stat.isDirectory()) {
            // Scan the directory recursive
            requireRoutes(path.join(dir, file), app);
        }
    });
}

var routes = function(app) {
    requireRoutes(__dirname, app);

    // Defines the root page. can be safely removed!
    app.get('/', function(req, res) {
        res.render('index', { mainRoutes : mainRoutes });
    });

    app.get('/showMacs', function(req, res) {
        res.render('showMac');
    });

    app.get('/help', function(req, res) {
        res.render('help');
    });

    app.get('/about', function(req, res) {
        res.render('about');
    });

    app.get('/showData', function(req, res) {
        res.send({'temp':currentTemp,'humid':currentHumid});
    });

    app.post('/showApp', function(req, res) {
        res.send(appStates);
    });

    app.get('/monitor',function(req,res){
        res.render('showTemp');
    });

    app.get('/control',function(req,res){
        res.render('control');
    });

    app.get('/userData',function(req,res){
        /*mongoose.connect("mongodb://localhost/database", function(err, db) {
          var collection = db.collection('user');
          console.log(collection.find().toArray(function(err, items) {}));
        });*/
        s = ''
        User.find({}, function (err, docs) {
            for(var i=0;i<docs.length;i++) s += docs[i]['bmac']+','
            res.send(s);
        });
    });

    app.get('/userName',function(req,res){
        /*mongoose.connect("mongodb://localhost/database", function(err, db) {
          var collection = db.collection('user');
          console.log(collection.find().toArray(function(err, items) {}));
        });*/
        s = ''
        User.find({}, function (err, docs) {
            for(var i=0;i<docs.length;i++) s += docs[i]['name']+','
            res.send(s);
        });
    });

    app.post('/temp',function(req,res) {
        currentTemp = req.query['temp'];
        currentHumid = req.query['humidity'];
        res.send("200 ok");
    });

    app.post('/postApp',function(req,res) {
        for(var i=0;i<4;i++) appStates[i] = toBool(req.query[i.toString()]);
        res.send("200 ok");
    });

    app.post('/actempblue',function(req,res) {
        acTemp = parseInt(req.query['actemp']);
        res.send("200 OK");
    });

    app.get('/atmg',function(req,res){
        res.send({'temp':acTemp});
    })

    app.get('/atb',function(req,res){
        res.send(acTemp.toString());
    });

    app.post('/actempmon',function(req,res){
        acTemp = parseInt(req.body['temp']);
        res.send("done!");
    });

    app.post('/postApp2',function(req,res) {
        for(var i=0;i<4;i++) appStates[i] = toBool(req.body[i.toString()]);
        //console.log(appStates);
        res.send("200 ok");
    });

    app.get('/data',function(req,res){
        res.send(appStates.join());
    });

    app.post('/nosPeople',function(req,res){
        nop = parseInt(req.query['nosPeople'])
        res.send("done");
    });

    app.get('/nosPeople2',function(req,res) {
        res.send(nop.toString());
    })

    app.post('/getbmac',function(req,res){
        res.send(allMacs);
    });
    app.post('/',function(req,res) {
        if(allMacs === "No Registered Users") allMacs=""; 
        allMacs = req.query['bmac']+"\n";
        res.send("200 ok");
    });
}

module.exports = routes;