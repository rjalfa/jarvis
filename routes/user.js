var User = require('../models/user'),
    mapper = require('../lib/model-mapper');

module.exports = function(app) {

    app.param('userId', function(req, res, next, id) {
        User.findById(id, function(err, user) {
            if (err) {
                next(err);
            } else {
                res.locals.user = user;
                next();
            }
        });
    });
    
    app.get('/users', function(req, res) {
        User.find({}, function(err, users) {
            res.render('user/index', { users : users });
        });
    });

    app.get('/users/create', function(req, res) {
        res.render('user/create', { user : new User() });
    });

    app.post('/users/create', function(req, res) { 
        var user = new User(req.body);

        user.save(function(err) {
            if (err) {
                res.render('user/create', {
                    user : user
                });
            } else {
                res.redirect('/users');
            }
        });
    });

    app.get('/users/:userId/edit', function(req, res) {
        res.render('user/edit');
    });

    app.post('/users/:userId/edit', function(req, res) {
        mapper.map(req.body).to(res.locals.user);

        res.locals.user.save(function(err) {
            if (err) {
                res.render('user/edit');
            } else {
                res.redirect('/users');
            }
        });
    });

    app.get('/users/:userId/detail', function(req, res) {
        res.render('user/detail');
    });

    app.get('/users/:userId/delete', function(req, res) {
        res.render('user/delete');
    });

    app.post('/users/:userId/delete', function(req, res) {
        User.remove({ _id : req.params.userId }, function(err) {
            res.redirect('/users');
        });
    });
}

// Used to build the index page. Can be safely removed!
module.exports.meta = {
    name : 'User',
    route : '/users'
}
