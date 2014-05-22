angular.module('user', ['restangular'])

.controller('UserDetail',
  function($scope, $stateParams, Restangular, $state) {
    $scope.endpoint = Restangular.one('users', $stateParams.username);
    $scope.user = $scope.endpoint.get().$object;

    $scope.go = function(state){
      $state.go(state);
    };
  })

.controller('UserFollowing',
  function($scope, Restangular) {
    var followx = $scope.endpoint.getList('following').$object;
    $scope.followx = followx;
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