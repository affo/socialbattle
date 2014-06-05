angular.module('logged', ['restangular'])

.controller('Logged',
  ['$scope', '$stateParams', 'Restangular', '$state', '$localStorage', '$modal',
  function($scope, $stateParams, Restangular, $state, $localStorage, $modal) {
    //check if logged
    // if(!$localStorage.logged){
    //   $state.go('unlogged');
    //   return;
    // }
    $scope.character_name = $localStorage.character;
    $scope.username = $localStorage.user; 

    if(!$localStorage.character){
      var modalInstance = $modal.open({
        templateUrl: 'selectCharacterModal.html',
        controller: 'SelectCharacterModal',
        backdrop: 'static',
        keyboard: false,
        resolve: {
          characters: function(){
            return Restangular.one('users', $localStorage.user).getList('characters').$object;
          },

          endpoint: function(){
            return Restangular.one('users', $localStorage.user).all('characters');
          }
        }
      });

      modalInstance.result.then(
        function(character){
          $scope.character_name = character;
        }
      );
    }
  }
  ]
)

.controller('SelectCharacterModal',
  ['$scope', '$modalInstance', '$localStorage', 'characters', 'endpoint',
  function($scope, $modalInstance, $localStorage, characters, endpoint){
    $scope.characters = characters;
    $scope.characterForm = {};
    $scope.alerts = [];

    $scope.create_character = function(){
      endpoint.post($scope.characterForm)
      .then(
        function(character){
          $scope.select(character);
        },
        function(response){
          $scope.alerts.push({type: 'danger', msg: response.data});
        }
      );
    };

    $scope.select = function(character){
      $localStorage.character = character.name;
      $modalInstance.close(character.name);
    };

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };
  }
  ]
);