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
              console.log('fb connected');
              var data = {access_token: response.authResponse.accessToken};

              Restangular.all('sa/associate/').customGET('facebook', data).then(
                function(user){
                  $localStorage.user = user.username;
                  $localStorage.facebook = true;
                }, function(response){
                  //error
                  console.log(response);
                });
          }else if(response.status === 'not_authorized'){
            // The person is logged into Facebook, but not your app.
            // and so I'm very sorry...
            console.log(response);
          } else {
            // The person is not logged into Facebook, so we're not sure if
            // they are logged into this app or not.
            // let's make him log in to Facebook
            Facebook.login(function(response){
              if(response.authResponse){
                $scope.ass_facebook();
              }else{
                //the user stopped the auth
              }
            }, {scope: 'publish_actions'});
          }
        });
      });
    };

  }
);