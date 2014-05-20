'use strict';

/* App Module */

var app = angular.module('socialBattle', [
  'ui.router',
  'restangular',
  'controllers',
  'facebook',
  'ngStorage',
  'auth',
]);

app.config(
  function(RestangularProvider){
    RestangularProvider.setBaseUrl('http://localhost.socialbattle:8000/private/');
    RestangularProvider.setRequestSuffix('/');
  });

app.config(['FacebookProvider', function(FacebookProvider) {
    // Here you could set your appId through the setAppId method and then initialize
    // or use the shortcut in the initialize method directly.
    FacebookProvider.init('1441968896050367');
}]);

app.config(
  function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/index');

    $stateProvider.

      state('home', {
        url: '/index',
        templateUrl: 'html/partials/home.html',
        controller: 'Auth',
      }).

      state('user-detail', {
        url: '/users/:username',
        templateUrl: 'html/partials/user-detail.html',
        controller: 'UserDetail'
      }).

      state('user-detail.follows', {
        url: '/follows',
        templateUrl: 'html/partials/user-detail.follows.html',
        controller: 'UserFollows'
      })
  });