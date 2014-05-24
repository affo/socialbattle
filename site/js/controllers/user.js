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

        Restangular.one('users', $localStorage.user.username)
          .customGET('following', {uname: user.username}).then(
            function(response){
              $scope.alreadyFollowing = true;
              $scope.fellowship = response.url;
            },
            function(response){
              $scope.alreadyFollowing = false;
            }
        );
      }
    );

    var update_user = function(){
      $localStorage.user = Restangular.one('users', $localStorage.user.username).get().$object;
    }

    $scope.follow = function(){
      data = {
        to_user: $scope.user.url,
      };
      $scope.endpoint.all('following').post(data).then(
        function(response){
          console.log(response);
          $scope.alreadyFollowing = true;
          $scope.fellowship = response.url;
          //update the stored user
          update_user();
        },
        function(response){
          console.log(response);
        }
      );
    };

    $scope.unfollow = function(){
      Restangular.oneUrl('fellowships', $scope.fellowship).remove().then(
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
)


.controller('UserFollowing',
  function($scope, Restangular) {
    $scope.followx = $scope.endpoint.getList('following').$object;
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