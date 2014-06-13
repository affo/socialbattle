angular.module('user', ['restangular'])

.controller('UserDetail',
  ['$scope', '$stateParams', 'Restangular', '$state', '$localStorage', 'user',
  function($scope, $stateParams, Restangular, $state, $localStorage, identity) {
    $scope.endpoint = Restangular.one('users', $stateParams.username);
    $scope.endpoint.get().then(
      function(user){
        $scope.user = user;
        if(user.username == identity.username){
          $scope.isMe = true;
        }

        Restangular.one('users', identity.username)
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
      Restangular.one('users', identity.username).all('following').post(data)
      .then(
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
    };
  }
  ]
)


.controller('UserFollowing',
  ['$scope', 'Restangular',
  function($scope, Restangular) {
    $scope.endpoint.getList('following')
    .then(
      function(response){
        var following = Restangular.stripRestangular(response);
        following = following.map(function(fellowship){
          return fellowship.to_user;
        });
        $scope.followx = following;
      }
    );
  }
  ]
)

.controller('UserFollowers',
  ['$scope', 'Restangular',
  function($scope, Restangular) {
    $scope.endpoint.getList('followers')
    .then(
      function(response){
        var followers = Restangular.stripRestangular(response);
        followers = followers.map(function(fellowship){
          return fellowship.from_user;
        });
        $scope.followx = followers;
      }
    );
  }
  ]
)

.controller('UserCharacters',
  ['$scope', 'Restangular', '$localStorage',
  function($scope, Restangular, $localStorage){
    var characters = $scope.endpoint.getList('characters').$object;
    $scope.characters = characters;
    $scope.characterForm = {};
    $scope.alerts = [];

    $scope.select = function(character){
      $localStorage.character = character.name;
    };

    $scope.create_character = function(){
      $scope.endpoint.all('characters').post($scope.characterForm)
      .then(
        function(character){
          $scope.characters.push(character);
          $scope.alerts.push({type: 'success', msg: character.name + ' succesfully created!'});
          $scope.characterForm = {};
        },
        function(response){
          $scope.alerts.push({type: 'danger', msg: response.data});
        }
      );
    };

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };
  }
  ]
);