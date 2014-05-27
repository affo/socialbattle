angular.module('settings', ['restangular', 'ngStorage', 'facebook'])

.controller('Settings',
  function($scope, $state, $localStorage, Restangular, Facebook){

  	$scope.logout = function(){ 
      $state.go('unlogged');
      Restangular.setDefaultHeaders(
          {'Authorization': ''}
      );
      delete $localStorage.token;
      delete $localStorage.logged;
      delete $localStorage.user;
      delete $localStorage.character;
      delete $localStorage.facebook;
      delete $localStorage.twitter;
      $state.go('unlogged');
    };

    $scope.ass_facebook = function(){
      console.log('getLoginStatus');
      Facebook.getLoginStatus(function(response){
        $scope.$apply(function(){
          if(response.status == 'connected') {
              var data = {access_token: response.authResponse.accessToken};

              Restangular.all('sa/associate/').customGET('facebook', data).then(
                function(user){
                  $localStorage.user = user;
                  $localStorage.facebook = true;
                }, function(response){
                  //error
                  console.log(response);
                });
          } else {
            //not logged to facebook
          };
        });
      });
    };

  }
);