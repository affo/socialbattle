var connect = require('connect');
var PORT = 3000;
var INDEX = 'html/index.html';

connect().use(connect.static(__dirname, {index: INDEX})).listen(PORT);
console.log('Connect server started...');
console.log('listening on localhost:3000...');