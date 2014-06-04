var connect = require('connect');
var PORT = 3000;
if(process.argv[2]){
	PORT = process.argv[2];
}
var INDEX = 'html/index.html';

connect().use(connect.static(__dirname, {index: INDEX})).listen(PORT);
console.log('Connect server started...');
console.log('listening on localhost:' + PORT + '...');