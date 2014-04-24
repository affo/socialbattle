'use strict';

/* App Module */

var app = angular.module('socialBattle', [
  'ui.router',
  'restangular',
  'controllers'
]);

app.config(
  function(RestangularProvider){
    RestangularProvider.setBaseUrl('http://localhost:8000/api/');
    RestangularProvider.setDefaultHeaders({
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'X-Requested-With',
      'withCredentials': 'true'
    });
  });

app.config(
  function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');

    $stateProvider.
      state('user-list', {
        url: '/users',
        templateUrl: 'html/partials/user-list.html',
        controller: 'UserList'
      }).

      state('user-detail', {
        url: '/users/:username',
        templateUrl: 'html/partials/user-detail.html',
        controller: 'UserDetail'
      }).

      state('home', {
        url: '/',
        templateUrl: 'html/partials/home.html'
      })
  });