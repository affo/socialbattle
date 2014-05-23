angular.module('user', ['restangular'])

.controller('UserDetail',
  function($scope, $stateParams, Restangular, $state, $localStorage, $http) {
    $scope.endpoint = Restangular.one('users', $stateParams.username);
    $scope.endpoint.get().then(
      function(user){
        $scope.user = user;
        if(user.url == $localStorage.user.url){
          $scope.isMe = true;
        }

        Restangular.one('users', $localStorage.user.username).getList('following').then(
          function(following){
            $scope.following = following;

            $scope.alreadyFollowing = false;
            for(var i = 0; i < following.length; i++){
              if(following[i].to_user.url == user.url) $scope.alreadyFollowing = true;
            }
          }
        );
      }
    );

    var update_user = function(){
      $localStorage.user = Restangular.one('users', $localStorage.user.username).get().$object;
    }

    $scope.go = function(state){
      $state.go(state);
    };

    $scope.follow = function(){
      data = {
        to_user: $scope.user.url,
      };
      $scope.endpoint.all('following').post(data).then(
        function(response){
          console.log(response);
          $scope.alreadyFollowing = true;
          //update the stored user
          update_user();
        },
        function(response){
          console.log(response);
        }
      );
    };

    $scope.unfollow = function(){
      var following = $scope.following;
      for(var i = 0; i < following.length; i++){
        console.log(following[i].to_user.url + " ---> " + $scope.user.url);
        if(following[i].to_user.url == $scope.user.url){
          Restangular.oneUrl('fellowships', following[i].url).remove().then(
            function(response){
              $scope.alreadyFollowing = false;
              //update the stored user
              update_user();
            },
            function(response){
              console.log(response);
            }

          );
        }
      }
    };
  })

.controller('UserFollowing',
  function($scope, Restangular) {
    $scope.endpoint.getList('following').then(
      function(following){
        var ret = Array();
        for(var i = 0; i < following.length; i++){
          ret.push(following[i].to_user);
        }
        $scope.followx = ret;
      },
      function(response){}
    );
    
  })

.controller('UserFollowers',
  function($http, $scope) {
    var followx = $scope.endpoint.getList('followers').$object;
    $scope.followx = followx;
  })

.controller('UserCharacters', function($scope, Restangular){
  var characters = $scope.endpoint.getList('characters').$object;
  $scope.characters = characters;
});