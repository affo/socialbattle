module.exports = function(grunt) {
  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    preprocess: {
      options: {
        context: process.env,
      },

      multifile: {
        files: {
          'js/app.js': 'js/app.raw.js',
          'js/services.js': 'js/services.raw.js',
        },
      },
    },

  });

  // Load the Grunt plugins.
  grunt.loadNpmTasks('grunt-preprocess');

  grunt.registerTask('default', ['preprocess', ]);
};