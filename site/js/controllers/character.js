angular.module('character', ['restangular'])

.controller('CharacterDetail',
  function($scope, $stateParams, Restangular, $state, $localStorage){
    $scope.endpoint = Restangular.one('characters', $stateParams.name);
    $scope.endpoint.get()
    .then(
      function(character){
        $scope.character = character;
      }
    );
  }
)

.controller('CharacterAbilities',
  function($scope, $stateParams, Restangular, $state, $localStorage){
    $scope.endpoint.getList('abilities').then(
      function(abilities){
        $scope.abilities = abilities;
      }
    );

    $scope.endpoint.getList('abilities/next').then(
      function(abilities){
        $scope.next_abilities = abilities;
      }
    );

  }
)

.controller('CharacterInventory',
  function($scope, $stateParams, Restangular, $state, $localStorage){
    $scope.endpoint.getList('inventory').then(
      function(inventory){
        $scope.inventory = inventory;
      }
    );

  }
);