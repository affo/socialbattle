angular.module('user', ['restangular'])

.controller('UserDetail',
  function($scope, $stateParams, Restangular) {
    $scope.user = Restangular.one('users', $stateParams.username).get().$object;
  })

.controller('UserFollows',
  function($http, $scope) {
    var urls = $scope.user.follows;
    console.log(urls);
    var follows = new Array();
    for(var i = 0; i < urls.length; i++){
        $http.get(urls[i]).then(
                function(result){
                    follows.push(result.data);
                });
    }
    $scope.follows = follows;
  });