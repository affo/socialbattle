angular.module('post', ['restangular'])

.controller('UserPosts', function($scope, Restangular){
  var posts = $scope.endpoint.getList('posts').$object;
  $scope.posts = posts;
  //add this to scope for inheriting states
  $scope.endpoint = Restangular.all('posts');
  $scope.commentForm = {};

  $scope.comment = function(post_id){
    $scope.endpoint.one(post_id).post($scope.commentForm).then(
      function(response){//success
      },
      function(response){//fail
      }
    );
  }
})

.controller('PostComments',
  function($scope, Restangular, $stateParams){
    $scope.comments = $scope.endpoint.one($stateParams.post_id).all('comments').getList().$object;
  }
);