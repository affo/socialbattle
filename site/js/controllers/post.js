angular.module('post', ['restangular'])

.controller('UserPosts',
  ['$scope', 'Restangular',
  function($scope, Restangular){
    $scope.can_post = false;
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
  }
  ]
)

.controller('RelaxRoomPosts',
  ['$scope', 'Restangular', '$localStorage', 'character', 'inventory',
  function($scope, Restangular, $localStorage, character, inventory){
    $scope.postForm = {
      exchanged_items: [],
      character: $localStorage.character.url
    };
    $scope.searched_items = [];
    $scope.alerts = [];
    $scope.can_post = true;
    $scope.character = character;
    $scope.inventory = inventory;

    var _number_given = 1;
    var _number_received = 1;

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };

    $scope.plus_given = function(){
      _number_given++;
      $scope.postForm.exchanged_items.push({given: true});
    };

    $scope.plus_received = function(){
      _number_received++;
      $scope.postForm.exchanged_items.push({given: false});
    };

    var keys = {
      LEFT: 37,
      UP: 38,
      RIGHT: 39,
      DOWN: 40,
      ENTER: 13,
      ESC: 27,
    };

    $scope.keypressed = function($event, $index){
      //console.log($event.which);
      var key = $event.which;
      if(key == keys.LEFT || key == keys.RIGHT){
        //does nothing
      }else if(key == keys.UP){

      }else if(key == keys.DOWN){

      }else{
        $scope.search($scope.postForm.exchanged_items[$index].item.name);
      }
    };

    $scope.search = function(query){
      if(!query) return;
      Restangular.all('items').customGET('', {query: query})
      .then(
        function(response){
          var items = Restangular.stripRestangular(response);
          $scope.searched_items = items;
        }
      );
    };

    $scope.select_given_item = function($item, $model, $label, $index){
      $scope.postForm.exchanged_items[$index].item = $item.item;
    };

    $scope.select_received_item = function($item, $model, $label, $index){
      $scope.postForm.exchanged_items[$index].item = $item;
    };

    $scope.post = function(){
      var post = $scope.postForm;
      if(post.give_guils && isNaN(post.give_guils)){
        $scope.alerts.push({type: "danger", msg: "Given guils must be a number!"});
        return;
      }
      if(post.receive_guils && isNaN(post.receive_guils)){
        $scope.alerts.push({type: "danger", msg: "Received guils must be a number!"});
        return;
      }

      for(var i = 0; i < post.exchanged_items.length; i++){
        var ex = post.exchanged_items[i];
        if(ex.quantity && isNaN(ex.quantity)){
          $scope.alerts.push({type: "danger", msg: "Quantity must be a number!"});
          return;
        }
      }

      post.exchanged_items = post.exchanged_items
      .filter(
        function(ex){
          if(ex.item){
            return true;
          }
          return false;
        }
      );

      post.exchanged_items = post.exchanged_items
      .map(
        function(ex){
          ex.item = ex.item.url;
          if(!ex.quantity) delete ex.quantity;
          if(!ex.given) delete ex.given;
          return ex;
        }
      );

      $scope.endpoint.all('posts').post(post).then(
        function(post){
          $scope.posts.unshift(post);
          $scope.postForm = {};
          $scope.given_items = [{}, ];
          $scope.received_items = [{}, ];
        },
        function(response){
          console.log(response);
          $scope.alerts.push({type: "danger", msg: response.data});
        }
      );
    };

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
  }
  ]
)

.controller('Post',
  ['$scope', 'Restangular',
  function($scope, Restangular){
    var character = $scope.character;
    var inventory = $scope.inventory;
    $scope.comment = {};
    $scope.searched_items = [];
    $scope.alerts = [];
    $scope.showing = false;
    $scope.editing = false;
    $scope.next = undefined;

    $scope.editPost = $scope.post;

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };

    var _number_given = 1;
    var _number_received = 1;

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };

    $scope.plus_given = function(){
      _number_given++;
      $scope.editPost.exchanged_items.push({given: true});
    };

    $scope.plus_received = function(){
      _number_received++;
      $scope.editPost.exchanged_items.push({given: false});
    };

    var acceptable = function(post){
      console.log(post); //rem
      if(!post.opened){
        return false;
      }

      if(post.character == character.url){
        return false;
      }
      //check guils!
      if(post.receive_guils > character.guils){
        return false;
      }

      exchanges = post.exchanged_items;
      var found = false;
      for(var i = 0; i < exchanges.length; i++){
        var ex = exchanges[i];
        if(!ex.given){
          for(var j = 0; j < inventory.length; j++){
            var record = inventory[j];
            if(record.item.url == ex.item && record.quantity < ex.quantity){
              return false;
            }
            if(record.item.url == ex.item && record.quantity >= ex.quantity){
              console.log('ok for item ' + record.item.name);
              found = true;
            }
          }

          if(!found){
            return false;
          }
          found = false;
        }
      }

      return true;
    }

    $scope.acceptable = acceptable($scope.post);

    $scope.toggle_editing = function(){
      $scope.editing = !$scope.editing;
      $scope.editPost = $scope.post;
      $scope.editPost.character = character.url;
    };

    var keys = {
      LEFT: 37,
      UP: 38,
      RIGHT: 39,
      DOWN: 40,
      ENTER: 13,
      ESC: 27,
    };

    $scope.keypressed = function($event, $index){
      //console.log($event.which);
      var key = $event.which;
      if(key == keys.LEFT || key == keys.RIGHT){
        //does nothing
      }else if(key == keys.UP){

      }else if(key == keys.DOWN){

      }else{
        $scope.search($scope.editPost.exchanged_items[$index].item.name);
      }
    };

    $scope.search = function(query){
      if(!query) return;
      Restangular.all('items').customGET('', {query: query})
      .then(
        function(response){
          var items = Restangular.stripRestangular(response);
          $scope.searched_items = items;
        }
      );
    };

    $scope.select_received_item = function($item, $model, $label, $index){
      $scope.editPost.exchanged_items[$index].item = $item;
    };

    $scope.select_given_item = function($item, $model, $label, $index){
      $scope.editPost.exchanged_items[$index].item = $item.item;
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
      var post = $scope.editPost;
      if(post.give_guils && isNaN(post.give_guils)){
        $scope.alerts.push({type: "danger", msg: "Given guils must be a number!"});
        return;
      }
      if(post.receive_guils && isNaN(post.receive_guils)){
        $scope.alerts.push({type: "danger", msg: "Received guils must be a number!"});
        return;
      }

      post.exchanged_items = post.exchanged_items
      .filter(
        function(ex){
          if(ex.item){
            return true;
          }
          return false;
        }
      );

      post.exchanged_items = post.exchanged_items
      .map(
        function(ex){
          ex.item = ex.item.url;
          if(!ex.quantity) delete ex.quantity;
          return ex;
        }
      );

      Restangular.oneUrl('post', post.url)
      .customPUT(post).then(
        function(post){
          //update what you are seeing
          $scope.post = Restangular.stripRestangular(post);
          $scope.editPost = $scope.post;
          $scope.toggle_editing();
        },
        function(response){
          console.log(response);
          $scope.alerts.push({type: "danger", msg: response.data});
        }
      );
    };

    $scope.accept = function(){
      Restangular.oneUrl('post', $scope.post.url)
      .all('accept')
      .post({character: $scope.character.url})
      .then(
        function(response){
          $scope.post = Restangular.stripRestangular(response);
          $scope.acceptable = false;
        },
        function(response){
          $scope.alerts.push({type: 'danger', msg: response.data});
        }
      );

    }

    $scope.load_comments = function(){
      Restangular.oneUrl('post', $scope.post.url).one('comments').get()
        .then(
          function(response){
            $scope.comments = response.results;
            $scope.showing = true;
            $scope.next = response.next;
          }
        );
    };

    $scope.remove_comments = function(){
      $scope.comments = {};
      $scope.showing = false;
    };

    $scope.submit = function(){
      Restangular.oneUrl('post', $scope.post.url).all('comments').post($scope.comment)
      .then(
        function(response){//success
          $scope.comment = {};
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
    };


  }
  ]
)

.controller('Comment', 
  ['$scope', 'Restangular',
  function($scope, Restangular){
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
  }
  ]
);