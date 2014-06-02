angular.module('auth', ['restangular', 'ngStorage', 'facebook'])

.controller('Auth',
  function($scope, Restangular, Facebook, $localStorage, $state) {
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
      console.log('getLoginStatus');
      Facebook.getLoginStatus(function(response){
        $scope.$apply(function(){
          if(response.status == 'connected') {
              console.log('fb connected');
              var data = {access_token: response.authResponse.accessToken};

              Restangular.all('sa/login/').customGET('facebook', data).then(
                function(response){
                  login(response.username, response.token, 'fb');
                }, function(response){
                  //error
                });
          } else {
            //not logged to facebook
          };
        });
      });
    }


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