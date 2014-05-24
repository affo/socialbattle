var httpProxy = require('http-proxy');
var PORT = 5000;

var proxy = httpProxy.createProxy();
var hosts = ['localhost.socialbattle', 'localhost.api.socialbattle'];

var options = {  
  'localhost.socialbattle': 'http://localhost:3000/',
  'localhost.api.socialbattle': 'http://localhost:8000/',
}

var server = require('http').createServer(function(req, res) {
  tg = req.headers.host.split(':')[0];
  //console.log(req.headers.host + ' ---> ' + options[tg]);
  if(tg == hosts[1]) req.url = '/public' + req.url;
  //console.log(req.url);
  proxy.web(req, res, {
    target: options[tg]
  });
});

console.log('Proxy server listening on port ' + PORT);
server.listen(PORT);