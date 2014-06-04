var pp = require('preprocess');
var src = 'js/app.raw.js'
var dest = 'js/app.js'

// Simple wrapper around fs.readFile and fs.writeFile
console.log('preprocessing ---> ' + process.env.HEROKU);
pp.preprocessFile(src, dest, process.env);