angular.module('post', ['restangular'])

.controller('UserPosts', function($scope, Restangular){
  //because of pagination
  $scope.endpoint.one('posts').get().then(
    function(response){
      $scope.posts = response.results;
      $scope.next = response.next;
    }
  );

  $scope.next_page = function(){
    Restangular.oneUrl('next_page', $scope.next).get().
    then(
      function(response){
        for(var i = 0; i < response.results.length; i++){
          $scope.posts.push(response.results[i]);
        }

        if(response.next){
          $scope.next = response.next;
        }else{
          $scope.next = undefined;
        }
      }
    );

  };
})

.controller('Post',
  function($scope, Restangular){
    $scope.comment = {};
    $scope.editPost = { content: $scope.post.content };
    $scope.showing = false;
    $scope.editing = false;
    $scope.next = undefined;

    $scope.toggle_editing = function(){
      $scope.editing = !$scope.editing;
    };

    $scope.delete_post = function(){
      var post_url = $scope.post.url;
      Restangular.oneUrl('post', post_url).remove()
      .then(
        function(response){
          for(var i = 0; i < $scope.posts.length; i++){
            if($scope.posts[i].url == post_url){
              $scope.posts.splice(i, 1);
            }
          }
        }
      );
    };

    $scope.edit_post = function(){
      var post =  Restangular.oneUrl('posts', $scope.post.url);
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

    $scope.load_comments = function(){
      Restangular.oneUrl('post', $scope.post.url).one('comments').get()
        .then(
          function(response){
            $scope.comments = response.results;
            $scope.showing = true;
            $scope.next = response.next;
          }
        );
    }

    $scope.remove_comments = function(){
      $scope.comments = {};
      $scope.showing = false;
    }

    $scope.submit = function(){
      Restangular.oneUrl('post', $scope.post.url).all('comments').post($scope.comment)
      .then(
        function(response){//success
          console.log(response);
          if($scope.showing){
            $scope.comments.unshift(response);
          }
        },
        function(response){//fail
          console.log(response);
        }
      );
    };

    $scope.next_page = function(){
    Restangular.oneUrl('next_page', $scope.next).get().
    then(
      function(response){
        for(var i = 0; i < response.results.length; i++){
          $scope.comments.push(response.results[i]);
        }

        if(response.next){
          $scope.next = response.next;
        }else{
          $scope.next = undefined;
        }
      }
      );
    }


  }
)

.controller('Comment', function($scope, Restangular){
  $scope.editing = false;
  $scope.editComment = { content: $scope.comment.content };

  $scope.toggle_editing = function(){
      $scope.editing = !$scope.editing;
  };

  $scope.delete_comment = function(){
    var comment_url = $scope.comment.url;
    Restangular.oneUrl('comment', comment_url).remove()
    .then(
      function(response){
        if($scope.showing){
          for(var i = 0; i < $scope.comments.length; i++){
            if($scope.comments[i].url == comment_url){
              $scope.comments.splice(i, 1);
            }
          }
        }
      }
    );
  };

  $scope.edit_comment = function(){
    var comment =  Restangular.oneUrl('comments', $scope.comment.url);
    console.log(comment);
    comment.content = $scope.editComment.content;
    comment.put().then(
      function(response){
        //update what you are seeing
        $scope.comment.content = comment.content;
        $scope.toggle_editing();
      }
    );
  };


});