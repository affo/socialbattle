angular.module('post', ['restangular'])

.controller('UserPosts', function($scope, Restangular){
  $scope.posts = $scope.endpoint.getList('posts').$object;
})

.controller('PostComments',
  function($scope, Restangular, $stateParams){
    $scope.comments = Restangular.one('posts', $stateParams.post_id).all('comments').getList().$object;

    $scope.comment = {};

    $scope.submit = function(post_id){
      console.log(post_id);
      console.log($scope.comment);
      Restangular.one('posts', post_id).all('comments').post($scope.comment).then(
        function(response){//success
          console.log(response);
          $scope.comments.push(response);
        },
        function(response){//fail
          console.log(response);
        }
      );
    }
  }
);