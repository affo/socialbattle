angular.module('logged', ['restangular'])

.controller('Logged',
  function($scope, $stateParams, Restangular, $state, $localStorage, $modal) {
    if(!$localStorage.character){
      var modalInstance = $modal.open({
        templateUrl: 'selectCharacterModal.html',
        controller: 'SelectCharacterModal',
        resolve: {
          characters: function(){
            return Restangular.one('users', $localStorage.user).getList('characters').$object;
          },

          endpoint: function(){
            return Restangular.one('users', $localStorage.user).all('characters');
          }
        }
      });
    }
  }
)

.controller('SelectCharacterModal',
  function($scope, $modalInstance, $localStorage, characters, endpoint){
    $scope.characters = characters;
    $scope.characterForm = {};

    $scope.create_character = function(){
      console.log($scope.characterForm);
      endpoint.post($scope.characterForm)
      .then(
        function(character){
          $scope.select(character);
        }
      );
    }

    $scope.select = function(character){
      $localStorage.character = character.name;
      $modalInstance.close();
    };
  }
);