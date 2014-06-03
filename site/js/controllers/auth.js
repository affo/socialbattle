angular.module('auth', ['restangular', 'ngStorage', 'facebook'])

.controller('Auth',
  function($scope, Restangular, $localStorage, Facebook, $state) {
    //if you are logged you cannot authenticate
    if($localStorage.logged){
      $state.go('user', {username: $localStorage.user});
    }

    $scope.$storage = $localStorage;
    $scope.alerts = [];
    $scope.signinForm = {};
    $scope.signupForm = {};

    var login = function(username, token, social){
      $localStorage.token = token;
      Restangular.setDefaultHeaders({'Authorization': 'Token ' + $localStorage.token});
      Restangular.one('users', username).get().then(
        function(user){
          $localStorage.user = user.username;
          $localStorage.logged = true;

          if(social == 'fb'){
            $localStorage.facebook = true;
          }else if(social == 'tw'){
            $localStorage.twitter = true;
          }

          $state.go('user.posts', {username: username});
        },
        function(response){
          $scope.alerts.push({type: 'danger', msg: response.data});
          $scope.signinForm = {};
        }
      );
    }

    $scope.fb_login = function() {
      Facebook.getLoginStatus(function(response){
        $scope.$apply(function(){
          if(response.status == 'connected') {
              console.log('fb connected');
              console.log(response.authResponse.accessToken);
              var data = {access_token: response.authResponse.accessToken};

              Restangular.all('sa/login/').customGET('facebook', data).then(
                function(response){
                  login(response.username, response.token, 'fb');
                }, function(response){
                  //error
                });
          }else if(response.status === 'not_authorized'){
            // The person is logged into Facebook, but not your app.
            // and so I'm very sorry...
          } else {
            // The person is not logged into Facebook, so we're not sure if
            // they are logged into this app or not.
            // let's make him log in to Facebook
            Facebook.login(function(response){
              if(response.authResponse){
                $scope.fb_login();
              }else{
                //the user stopped the auth
              }
            }, {scope: 'publish_actions'});
          }
        });
      });
    };


    $scope.sb_login = function(){
        var data = {
            username: $scope.signinForm.username,
            password: $scope.signinForm.password,
        };

        Restangular.all('auth').post(data).then(
            function(response){
                console.log(response);
                login(data.username, response.token, '');
            },
            function(response){
                console.log(response);
                $scope.alerts.push({type: 'danger', msg: response.data});
            });
    };

    $scope.signup = function(){
        var data = {
            username: $scope.signupForm.username,
            email: $scope.signupForm.email,
            password: $scope.signupForm.password,
        };

        var check = $scope.signupForm.check_password;

        if(check != data.password){
          $scope.alerts.push({type: 'danger', msg: 'The two passwords are different!'});
          $scope.signupForm.password = '';
          $scope.signupForm.check_password = '';
          return;
        }

        Restangular.all('signup').post(data).then(
            function(response){
                $scope.alerts.push({type: 'success', msg: 'Succesfully signed up!'});
                $scope.signupForm = {};
            },
            function(response){
                $scope.alerts.push({type: 'danger', msg: response.data});
            });
    };

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };
});