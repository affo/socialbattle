angular.module('auth', ['restangular', 'ngStorage', 'facebook'])

.controller('Auth',
  function($scope, Restangular, Facebook, $localStorage, $state) {
    //if you are logged you cannot authenticate
    if($localStorage.logged){
      $state.go('user', {username: $localStorage.user.username});
    }

    $scope.$storage = $localStorage;
    $scope.signinForm = {};
    $scope.signupForm = {};
    // Here, usually you should watch for when Facebook is ready and loaded
    $scope.$watch(function() {
      return Facebook.isReady(); // This is for convenience, to notify if Facebook is loaded and ready to go.
    }, function(newVal) {
      $scope.facebookReady = true; // You might want to use this to disable/show/hide buttons and else
    });

    var login = function(username, token){
      $localStorage.token = token;
      Restangular.setDefaultHeaders({'Authorization': 'Token ' + $localStorage.token});
      $localStorage.logged = $localStorage.token !== undefined;
      $localStorage.user = Restangular.one('users', username).get().$object;
      $state.go('user.posts', {username: username});
    }

    $scope.fb_login = function() {
      console.log('getLoginStatus');
      Facebook.getLoginStatus(function(response){
        $scope.$apply(function(){
          if(response.status == 'connected') {
              $localStorage.logged = true;
              console.log(response);
              var data = {access_token: response.authResponse.accessToken};

              Restangular.all('sa/register/').customGET('facebook', data).then(
                function(response){
                  console.log(response);
                  login(response.username, response.token);
                }, function(response){
                  //error
                  console.log(response);
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

        console.log(data);

        Restangular.all('auth').post(data).then(
            function(response){
                console.log(response);
                login(data.username, response.token);
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