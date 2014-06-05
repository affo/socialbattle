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

    concat: {
      js: {
        src: [
          'js/app.js',
          'js/app-states.js',
          'js/services.js',
          'js/controllers/*',
        ],

        dest: 'js/socialbattle.js',
      }
    },

    uglify : {
      js: {
        files: {
            'js/socialbattle.min.js' : 'js/socialbattle.js',
        },
      },
    },

    jshint: {
      app: 'js/app.raw.js',
      states: 'js/app-states.js',
      services: 'js/services.raw.js',
      auth: 'js/controllers/auth.js',
      character: 'js/controllers/character.js',
      logged: 'js/controllers/logged.js',
      main: 'js/controllers/main.js',
      post: 'js/controllers/post.js',
      room: 'js/controllers/room.js',
      search: 'js/controllers/search.js',
      settings: 'js/controllers/settings.js',
      user: 'js/controllers/user.js',

      all: [
        'js/app.raw.js',
        'js/app-states.js',
        'js/services.raw.js',
        'js/controllers/auth.js',
        'js/controllers/character.js',
        'js/controllers/logged.js',
        'js/controllers/main.js',
        'js/controllers/post.js',
        'js/controllers/room.js',
        'js/controllers/search.js',
        'js/controllers/settings.js',
        'js/controllers/user.js',
      ],
    },

  });

  // Load the Grunt plugins.
  grunt.loadNpmTasks('grunt-preprocess');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');

  grunt.registerTask('default', ['preprocess', 'concat', 'uglify', ]);
};