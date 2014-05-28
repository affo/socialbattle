angular.module('user', ['restangular'])

.controller('UserDetail',
  function($scope, $stateParams, Restangular, $state, $localStorage) {
    $scope.endpoint = Restangular.one('users', $stateParams.username);
    $scope.endpoint.get().then(
      function(user){
        $scope.user = user;
        if(user.username == $localStorage.user){
          $scope.isMe = true;
        }

        Restangular.one('users', $localStorage.user)
          .post('isfollowing', {to_user: user.url}).then(
            function(response){
              $scope.alreadyFollowing = response.is_following;
              $scope.fellowship = response.url;
            },
            function(response){
              $scope.alreadyFollowing = false;
            }
        );
      }
    );

    $scope.follow = function(){
      data = {
        to_user: $scope.user.url,
      };
      $scope.endpoint.all('following').post(data).then(
        function(response){
          console.log(response);
          $scope.alreadyFollowing = true;
          $scope.fellowship = response.url;
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
  function($scope) {
    var followx = $scope.endpoint.getList('followers').$object;
    $scope.followx = followx;
  })

.controller('UserCharacters', function($scope, Restangular, $localStorage){
  var characters = $scope.endpoint.getList('characters').$object;
  $scope.characters = characters;
  $scope.characterForm = {};

  $scope.select = function(character){
    $localStorage.character = character.name;
  }

  $scope.create_character = function(){
    console.log($scope.characterForm);
    $scope.endpoint.all('characters').post($scope.characterForm)
    .then(
      function(character){
        $scope.characters.push(character);
      }
    );
  }
});