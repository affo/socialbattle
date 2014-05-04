'use strict';

/* Controllers */

var ctrls = angular.module('controllers', ['restangular']);

ctrls.controller('UserList',
  function($scope, Restangular) {
    $scope.users = Restangular.all('users').getList().$object;
  });

ctrls.controller('UserDetail',
  function($scope, $stateParams, Restangular) {
    $scope.user = Restangular.one('users', $stateParams.username).get().$object;
  });

ctrls.controller('UserFollows',
  function($http, $scope) {
    var urls = $scope.user.follows;
    console.log(urls);
    var follows = new Array();
    for(var i = 0; i < urls.length; i++){
        $http.get(urls[i]).then(
                function(result){
                    follows.push(result.data);
                });
    }
    $scope.follows = follows;
  });

ctrls.controller('Home',
  function($scope, Restangular) {
    $scope.logged = false;
    $scope.signinForm = {};
    $scope.signupForm = {};
    $scope.user = {};

    $scope.signin = function(){
        var data = {
            username: $scope.signinForm.username,
            password: $scope.signinForm.password,
        };

        console.log(data);

        Restangular.all('sign/in').post(data).then(
            function(response){
                console.log(response);
                Restangular.setDefaultHeaders(
                    {'Authorization': 'Token ' + response.token}
                )
                $scope.logged = true;
            },
            function(response){
                console.log(response);
            });
    };

    $scope.signup = function(){
        var data = {
            username: $scope.signupForm.username,
            email: $scope.signupForm.email,
            password: $scope.signupForm.password,
        };

        console.log(data);

        Restangular.all('sign/up').post(data).then(
            function(response){
                console.log(response);
            },
            function(response){
                console.log(response);
            });
    };

    $scope.signout = function(){
        Restangular.all('sign/out').post().then(
            function(response){
                console.log(response);
                Restangular.setDefaultHeaders(
                    {'Authorization': ''}
                )
                $scope.logged = false;
            },
            function(response){
                console.log(response);
            });
    };
  });