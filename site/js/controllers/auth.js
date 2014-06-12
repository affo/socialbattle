angular.module('auth', ['restangular', 'ngStorage', 'facebook'])

.controller('Auth',
  ['$scope', 'Restangular', '$localStorage', 'Facebook', '$state', 'LoginService',
  function($scope, Restangular, $localStorage, Facebook, $state, LoginService) {
    //if you are logged you cannot authenticate
    if($localStorage.logged){
      $state.go('user', {username: $localStorage.user});
    }

    $scope.$storage = $localStorage;
    $scope.alerts = [];
    $scope.signinForm = {};
    $scope.signupForm = {};

    $scope.fb_login = function(){
      LoginService.fb_login()
      .then(
        function(result){
          $state.go('logged');
        },
        function(response){
          $scope.alerts.push({type: 'danger', msg: response.data});
        }
      );
    };


    $scope.sb_login = function(){
        LoginService.sb_login($scope.signinForm.username, $scope.signinForm.password)
        .then(
          function(result){
            $state.go('logged');
          },
          function(response){
            $scope.alerts.push({type: 'danger', msg: response.data});
          }
        );
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
  }
  ]
);