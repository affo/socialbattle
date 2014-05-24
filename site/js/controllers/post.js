angular.module('post', ['restangular'])

.controller('UserPosts', function($scope, Restangular){
  $scope.posts = $scope.endpoint.getList('posts').$object;
  $scope.post_selected = 0;
})

.controller('PostComments',
  function($scope, Restangular){
    $scope.comment = {};
    $scope.showing = false;

    $scope.load_comments = function(post_id){
      Restangular.one('posts', post_id).all('comments').getList()
        .then(
          function(comments){
            $scope.comments = comments;
            $scope.showing = true;
          }
        );
    }

    $scope.remove_comments = function(){
      $scope.comments = {};
      $scope.showing = false;
    }

    $scope.submit = function(post_id){
      Restangular.one('posts', post_id).all('comments').post($scope.comment)
      .then(
        function(response){//success
          console.log(response);
          if($scope.comments){
            $scope.comments.push(response);
          }
        },
        function(response){//fail
          console.log(response);
        }
      );
    }
  }
);