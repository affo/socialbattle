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
    RestangularProvider.setRequestSuffix('/');
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
      }).

      state('user-detail.follows', {
        url: '/follows',
        templateUrl: 'html/partials/user-detail.follows.html',
        controller: 'UserFollows'
      })
  });