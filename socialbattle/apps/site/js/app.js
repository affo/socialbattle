'use strict';

/* App Module */

var app = angular.module('wordsApp', [
  'ui.router',
  'wordsControllers'
]);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.config(
  function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/words");

    $stateProvider.
      state('list', {
        url: '/words',
        templateUrl: '/apps/site/html/partials/word-list.html',
        controller: 'WordList'
      }).

      state('detail', {
        url: '/words/:word_id',
        templateUrl: '/apps/site/html/partials/word-detail.html',
        controller: 'WordDetail'
      })
  });