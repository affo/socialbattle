'use strict';
var auth = angular.module('auth', ['restangular', 'ngStorage', 'facebook']);

auth.controller('Auth',
  function($scope, Restangular, Facebook, $localStorage, $location) {
    $scope.$storage = $localStorage;
    $scope.signinForm = {};
    $scope.signupForm = {};
    console.log('this is the user in webstorage');
    console.log($scope.user);
    // Here, usually you should watch for when Facebook is ready and loaded
    $scope.$watch(function() {
      return Facebook.isReady(); // This is for convenience, to notify if Facebook is loaded and ready to go.
    }, function(newVal) {
      $scope.facebookReady = true; // You might want to use this to disable/show/hide buttons and else
    });

    $scope.getLoginStatus = function() {
      console.log('getLoginStatus');
      Facebook.getLoginStatus(function(response) {
        if(response.status == 'connected') {
          $scope.$apply(function() {
            $scope.logged = true;
            $scope.me();
            console.log(response)
            var data = {
              access_token: response.authResponse.accessToken
            };
            console.log(data);
            Restangular.all('sa/register/').customGET('facebook', data).then(
              function(response){
                console.log(response);
              }
            );
          });
        }
        else {
          $scope.$apply(function() {
            $scope.logged = false;
          });
        }
      })};

      $scope.me = function() {
        Facebook.api('/me', function(response) {
          $scope.$apply(function() {
            // Here you could re-check for user status (just in case)
            $scope.user = response;
          });
        });
      };


    $scope.signin = function(){
        var data = {
            username: $scope.signinForm.username,
            password: $scope.signinForm.password,
        };

        console.log(data);

        Restangular.all('auth').post(data).then(
            function(response){
                console.log(response);
                $localStorage.token = response.token;
                $localStorage.logged = true;
                Restangular.setDefaultHeaders({'Authorization': 'Token ' + $localStorage.token});
                var user = Restangular.all('users').get(data.username).$object;
                $localStorage.user = user;
                $location.path('/users/' + data.username);
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

        Restangular.all('users').post(data).then(
            function(response){
                console.log(response);
            },
            function(response){
                console.log(response);
            });
    };
});

auth.controller('NavBar',
function($scope, Restangular, $localStorage, $location){
  if($localStorage.token){
      Restangular.setDefaultHeaders({'Authorization': 'Token ' + $localStorage.token});
  }
  $scope.$storage = $localStorage;

  $scope.logout = function(){ 
      var username = $localStorage.user.username;
      Restangular.setDefaultHeaders(
          {'Authorization': ''}
      );
      delete $localStorage.token;
      delete $localStorage.logged;
      delete $localStorage.user;
      $location.path('/');
    };
});