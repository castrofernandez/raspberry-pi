var express = require('express');
var app = express();
var expressHbs = require('express-handlebars');
var request = require("request");
var parseString = require('xml2js').parseString;
var http = require('http');
var fs = require('fs');
var path = require('path');

app.engine('hbs', expressHbs({extname:'hbs', defaultLayout:'main.hbs'}));
app.set('view engine', 'hbs');

app.get('/', function(req, res) {
  var rss = "http://www.applesfera.com/index.xml";

  request({
    url: rss,
    json: true
    }, function (error, response, body) {
        if (!error && response.statusCode === 200) {
          parseString(body, function (err, result) {
            var objeto = result.rss.channel[0];
            var titulo = objeto.title;
            var noticias = objeto.item;

            findImages(noticias);

            var data = {
              "noticias": noticias
            };

            res.render('index', data);
          });
        }
    });
});

function findImages(noticias) {
  var re = /<img[^>]+src="?([^"\s]+)"?[^>]*>/g;

  for (var i = 0; i < noticias.length; i++) {
    var noticia = noticias[i].description[0];

    while (m = re.exec(noticia)) {
      var src = m[1];

      var dot = src.lastIndexOf(".");
      var extension = src.substring(dot + 1);

      var ruta = path.join(__dirname, "/images/file." + extension);
      var fichero = fs.createWriteStream(ruta);

      var peticion = http.get(src, function(respuesta) {
        respuesta.pipe(fichero);
      });
    }
  }
}

var server = app.listen(3000, function() {
    console.log('Listening on port %d', server.address().port);
});
