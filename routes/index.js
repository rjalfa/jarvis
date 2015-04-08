var path = require('path'),
    fs = require('fs');


var allMacs = "No macs"    
var currentTemp = "0";
var mainRoutes = [];

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
        res.send(allMacs);
    });

    app.get('/showData', function(req, res) {
        res.send(currentTemp);
    });

    app.get('/monitor',function(req,res){
        res.render('showTemp');
    });

    app.get('/control',function(req,res){
        res.render('control');
    });

    app.post('/temp',function(req,res) {
        currentTemp = req.query['temp'];
        res.send("200 ok");
    });

    app.post('/',function(req,res) {
        console.log(req.query['bmac']);
        allMacs = (req.query['bmac']);
        res.send("200 ok");
    })
}

module.exports = routes;
