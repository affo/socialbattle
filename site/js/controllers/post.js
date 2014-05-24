angular.module('post', ['restangular'])

.controller('UserPosts', function($scope, Restangular){
  $scope.posts = $scope.endpoint.getList('posts').$object;
  $scope.post_selected = 0;
})

.controller('Post',
  function($scope, Restangular){
    $scope.comment = {};
    $scope.editPost = { content: $scope.post.content };
    $scope.showing = false;
    $scope.editing = false;

    $scope.toggle_editing = function(){
      $scope.editing = !$scope.editing;
    }

    $scope.delete_post = function(post_id){
      Restangular.one('posts', post_id).remove()
      .then(
        function(response){
          for(var i = 0; i < $scope.posts.length; i++){
            if($scope.posts[i].id == post_id){
              $scope.posts.splice(i, 1);
            }
          }
        }
      );
    };
    $scope.edit_post = function(post_id){
      var post =  Restangular.one('posts', post_id);
      console.log(post);
      post.content = $scope.editPost.content;
      post.put().then(
        function(response){
          //update what you are seeing
          $scope.post.content = post.content;
          $scope.toggle_editing();
        }
      );
    };

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
          if($scope.showing){
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