angular.module('user', ['restangular'])

.controller('UserDetail',
  function($scope, $stateParams, Restangular) {
    $scope.endpoint = Restangular.one('users', $stateParams.username);
    $scope.user = $scope.endpoint.get().$object;
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

.controller('UserPosts', function($scope, Restangular){
  var posts = $scope.endpoint.getList('posts').$object;
  $scope.posts = posts;
})

.controller('UserCharacters', function($scope, Restangular){

});