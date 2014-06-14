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
  ['$scope', 'Restangular', '$localStorage',
  function($scope, Restangular, $localStorage){
    $scope.postForm = {};
    $scope.given_items = [{}, ];
    $scope.received_items = [{}, ];
    $scope.searched_items = [];
    $scope.selected_received_items = [];
    $scope.selected_given_items = [];
    $scope.alerts = [];
    $scope.can_post = true;

    var _number_given = 1;
    var _number_received = 1;

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };

    $scope.plus_given = function(){
      _number_given++;
      $scope.given_items.push({});
    };

    $scope.plus_received = function(){
      _number_received++;
      $scope.received_items.push({});
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
        $scope.search($scope.received_items[$index].item_name);
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
      $scope.selected_received_items[$index] = $item;
    };

    $scope.select_given_item = function($item, $model, $label, $index){
      $scope.selected_given_items[$index] = $item;
    };

    $scope.post = function(){
      //aliases
      var given_items = $scope.given_items;
      var received_items = $scope.received_items;
      var exchanged_items = [];

      if($scope.postForm.give_guils && isNaN($scope.postForm.give_guils)){
        $scope.alerts.push({type: "danger", msg: "Given guils must be a number!"});
        return;
      }
      if($scope.postForm.receive_guils && isNaN($scope.postForm.receive_guils)){
        $scope.alerts.push({type: "danger", msg: "Received guils must be a number!"});
        return;
      }

      var find_item = function(item_name){
        for(i = 0; i < $scope.sell_items.length; i++){
          if(item_name == $scope.sell_items[i].item.name){
            return $scope.sell_items[i].item;
          }
        }
        return undefined;
      };

      for(var i = 0; i < $scope.given_items.length; i++){
        var items = $scope.selected_given_items;
        if(items[i]){
          var quantity = received_items[i].quantity;
          if(quantity && isNaN(quantity)){
            $scope.alerts.push({type: "danger", msg: "Quantity must be a number!"});
            return;
          }
          exchanged_items.push({
            given: true,
            item: items[i].url,
            quantity: quantity,
          });
        }
      }

      for(var i = 0; i < $scope.received_items.length; i++){
        var items = $scope.selected_received_items;
        if(items[i]){
          var quantity = received_items[i].quantity;
          if(quantity && isNaN(quantity)){
            $scope.alerts.push({type: "danger", msg: "Quantity must be a number!"});
            return;
          }
          exchanged_items.push({
            given: false,
            item: items[i].url,
            quantity: quantity,
          });
        }
      }

      var data = {
        content: $scope.postForm.content,
        character: $localStorage.character.url,
        exchanged_items: exchanged_items,
        give_guils: $scope.postForm.give_guils,
        receive_guils: $scope.postForm.receive_guils,
      }

      $scope.endpoint.all('posts').post(data).then(
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
    $scope.comment = {};
    $scope.searched_items = [];

    var init_post_vars = function(post){
      var _given_items = post.exchanged_items
      .filter(
        function(exchange){
          return exchange.given;
        }
      );
      var _received_items = post.exchanged_items
      .filter(
        function(exchange){
          return !exchange.given;
        }
      );
      $scope.given_items = _given_items.map(
        function(exchange){
            return {item_name: exchange.item, quantity: exchange.quantity};
        }
      );
      $scope.received_items = _received_items.map(
        function(exchange){
          return {item_name: exchange.item, quantity: exchange.quantity};
        }
      );
      $scope.selected_received_items = _received_items.map(
        function(exchange){
          return exchange.item;
        }
      );
    }
    init_post_vars($scope.post);
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
      $scope.given_items.push({});
    };

    $scope.plus_received = function(){
      _number_received++;
      $scope.received_items.push({});
    };

    $scope.toggle_editing = function(){
      $scope.editing = !$scope.editing;
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
        $scope.search($scope.received_items[$index].item_name);
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

    $scope.select_item = function($item, $model, $label, $index){
      $scope.selected_received_items[$index] = $item;
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
      var given_items = $scope.given_items;
      var received_items = $scope.received_items;
      var exchanged_items = [];

      if($scope.editPost.give_guils && isNaN($scope.editPost.give_guils)){
        $scope.alerts.push({type: "danger", msg: "Given guils must be a number!"});
        return;
      }
      if($scope.editPost.receive_guils && isNaN($scope.editPost.receive_guils)){
        $scope.alerts.push({type: "danger", msg: "Received guils must be a number!"});
        return;
      }

      var find_item = function(item_name){
        for(i = 0; i < $scope.sell_items.length; i++){
          if(item_name == $scope.sell_items[i].item.name){
            return $scope.sell_items[i].item;
          }
        }
        return undefined;
      };

      for(var i = 0; i < $scope.given_items.length; i++){
        if(given_items[i].item_name){
          var item = find_item(given_items[i].item_name);
          if(!item){
            $scope.alerts.push({type: "danger", msg: "Item not found!"});
            return;
          }
          var quantity = given_items[i].quantity;
          if(quantity && isNaN(quantity)){
            $scope.alerts.push({type: "danger", msg: "Quantity must be a number!"});
            return;
          }
          exchanged_items.push({
            given: true,
            item: item.url,
            quantity: quantity,
          });
        }
      }

      for(var i = 0; i < $scope.received_items.length; i++){
          var items = $scope.selected_received_items;
        if(items[i]){
          var quantity = received_items[i].quantity;
          if(quantity && isNaN(quantity)){
            $scope.alerts.push({type: "danger", msg: "Quantity must be a number!"});
            return;
          }
          exchanged_items.push({
            given: false,
            item: items[i].url,
            quantity: quantity,
          });
        }
      }

      var post = Restangular.oneUrl('posts', $scope.post.url);
      post.content = $scope.editPost.content;
      post.receive_guils = $scope.editPost.receive_guils;
      post.give_guils = $scope.editPost.give_guils;
      post.exchanged_items = exchanged_items;
      post.character = $scope.post.character;
      post.put().then(
        function(post){
          //update what you are seeing
          $scope.post = Restangular.stripRestangular(post);
          init_post_vars($scope.post);
          $scope.toggle_editing();
        },
        function(response){
          console.log(response);
          $scope.alerts.push({type: "danger", msg: response.data});
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
    };

    $scope.remove_comments = function(){
      $scope.comments = {};
      $scope.showing = false;
    };

    $scope.submit = function(){
      Restangular.oneUrl('post', $scope.post.url).all('comments').post($scope.comment)
      .then(
        function(response){//success
          console.log(response);
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