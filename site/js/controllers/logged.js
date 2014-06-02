angular.module('logged', ['restangular'])

.controller('Logged',
  function($scope, $stateParams, Restangular, $state, $localStorage, $modal) {
    //check if logged
    if(!$localStorage.logged){
      $state.go('unlogged');
      return;
    }

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
    }
  }
)

.controller('SelectCharacterModal',
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
    }

    $scope.select = function(character){
      $localStorage.character = character.name;
      $modalInstance.close();
    };

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };
  }
);