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
    $urlRouterProvider.otherwise("/users");

    $stateProvider.
      state('list', {
        url: '/users',
        templateUrl: '/apps/site/html/partials/user-list.html',
        controller: 'UserList'
      }).

      state('detail', {
        url: '/users/:user_id',
        templateUrl: '/apps/site/html/partials/user-detail.html',
        controller: 'UserDetail'
      })
  });

/*app.config(
  function(RestangularProvider){
      RestangularProvider.setDefaultHeaders({'Authorization': 'Basic root:root'});
  });*/