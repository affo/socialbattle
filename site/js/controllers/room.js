angular.module('room', ['luegg.directives'])

.controller('Rooms',
  function($scope, $state, $localStorage, Restangular){
    $scope.pverooms = Restangular.all('rooms/pve').getList().$object;
    $scope.relaxrooms = Restangular.all('rooms/relax').getList().$object;
    $scope.go = function(string, data){
      $state.go(string, data);
    };
})

.controller('PVERoom',
  function($scope, Restangular, $stateParams, $localStorage, SpawnService, MobService, CharacterService,
            character, character_abilities, character_inventory, mobs){
    $scope.messages = [];
    $scope.character = character;
    //$scope.character.abilities = character_abilities;
    //$scope.character.inventory = character_inventory;
    $scope.room = room;

    var mob_attack = function(){
      return $scope.mob_abilities_promise
      .then(
        function(response){
          var abilities = Restangular.stripRestangular(response);
          return MobService.attack($scope.mob.slug, $scope.character.url, abilities);
        }
      );
    }

    SpawnService.spawn(mobs).then(
      function(mob){
        $scope.mob = mob;
        $scope.mob_abilities_promise = Restangular.one('mobs', mob.slug).getList('abilities');
        $scope.messages.push(mob.name);
        return mob;
      }
    );
})

.controller('RelaxRoom', function($scope, Restangular, $stateParams, $localStorage, $modal){
  $scope.endpoint = Restangular.one('rooms/relax', $stateParams.room_name);
  $scope.character_endpoint = Restangular.one('characters', $localStorage.character);
  $scope.character = $scope.character_endpoint.get().$object;
  $scope.init_msg = 'Welcome, I am the merchant at ' + $stateParams.room_name;
  $scope.buy_items = $scope.endpoint.all('items').getList().$object;
  $scope.msgForm = {};
  $scope.action = 'BUY';

  $scope.toggle_action = function(){
    if($scope.action == 'BUY'){
      $scope.action = 'SELL';
      $scope.sell_items = $scope.character_endpoint.getList('inventory').$object;
    }else{
      $scope.action = 'BUY';
    }
    ai.reset();
  }

  var ai = {
    find_item: function(item_name){
      //find the item by name
      if($scope.action == 'BUY'){
        for(var i = 0; i < $scope.buy_items.length; i++){
          if(item_name == $scope.buy_items[i].name){
            return $scope.buy_items[i];
          }
        }
        return undefined;
      }else if($scope.action == 'SELL'){
        for(var i = 0; i < $scope.sell_items.length; i++){
          if(item_name == $scope.sell_items[i].item.name){
            return $scope.sell_items[i].item;
          }
        }
        return undefined;
      }
    },

    reset: function(){
      var msg = {
        content: 'Please type the item you want to ' + $scope.action,
        from_merchant: true,
      };
      $scope.messages.push(msg);
      $scope.state = ai.INIT;
    },

    INIT: function(item_name){
      item = ai.find_item(item_name);

      if(item){
        $scope.selected_item = item;
        var msg = {
          content: 'So you want to ' + $scope.action + ' ' + item_name + '... How many?',
          from_merchant: true,
        };
        $scope.messages.push(msg);
        $scope.state = ai.HOW_MANY;
      }else{
        var content = '';
        if($scope.action == 'BUY'){
          content = 'I do not sell ' + item_name + ', sorry...';
        }else{
          content = 'You do not have ' + item_name + ' in your inventory';
        }
        var msg = {
          content: content,
          from_merchant: true,
        };
        $scope.messages.push(msg);
      }
    },

    HOW_MANY: function(quantity){
      if(isNaN(quantity)){
        var msg = {
          content: 'Please give me a valid number',
          from_merchant: true,
        };
      }else{
        var msg = {
            content: 'So you want to ' + $scope.action + ' ' + quantity + " of " + $scope.selected_item.name,
            from_merchant: true,
          };
        $scope.messages.push(msg);

        var data = {
          item: $scope.selected_item.url,
          quantity: quantity,
          operation: $scope.action[0]
        };

        $scope.character_endpoint.all('transactions').post(data)
        .then(
          function(response){
            ai.OK(response);
          },
          function(response){
            console.log(response);
            ai.KO(response);
          }
        );
      }
    },

    OK: function(resp){
      var msg = {
          content: "Well done",
          from_merchant: true,
      };
      $scope.character.guils = resp.guils_left;
      $scope.messages.push(msg);
      $scope.transaction_ended(msg.content);

      if($scope.action == 'SELL'){
        $scope.sell_items = $scope.character_endpoint.getList('inventory').$object;
      }
    },

    KO: function(resp){
      var msg = {
          content: resp.data.msg,
          from_merchant: true,
      };
      $scope.messages.push(msg);
      ai.reset();
    },
  }

  $scope.endpoint.get().then(
    function(room){
      var init_msg = {
        content: 'Welcome, I am the merchant at ' + room.name,
        from_merchant: true
      };
      $scope.messages = [init_msg, ];
      ai.reset();
    }
  );

  $scope.ai = ai;
  $scope.state = ai.INIT;

  $scope.send = function(){
    var msg = $scope.msgForm.content
    var sent = {
      content: msg,
      from_user: true,
    };
    $scope.messages.push(sent);
    $scope.state(msg);
    $scope.msgForm = {};
  };

  $scope.put_item = function(name){
    $scope.msgForm.content = name;
  };

  $scope.transaction_ended = function(){
    var modalInstance = $modal.open({
      templateUrl: 'transactionModal.html',
      controller: 'TransactionModal',
      resolve: {
        user: function (){
          return $localStorage.user;
        },

        character: function(){
          return $localStorage.character;
        },

        item: function(){
          return $scope.selected_item.name;
        },

        shop: function(){
          return $stateParams.room_name;
        },

        action: function(){
          if($scope.action == 'BUY'){
            return 'bought';
          }
          return 'sold';
        },
      }
    });

    modalInstance.result
    .then(
      function() {
        ai.reset();
      }
    );

  };

})

.controller('RelaxRoomPosts', function($scope, Restangular){
  $scope.postForm = {};
  $scope.can_post = true;

  $scope.post = function(){
    $scope.endpoint.all('posts').post($scope.postForm).then(
      function(post){
        $scope.posts.unshift(post);
        $scope.postForm = {};
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
})

.controller('TransactionModal', function($scope, $modalInstance, user, action, character, shop, item){

    $scope.user = user;
    $scope.action = action;
    $scope.character = character;
    $scope.shop = shop;
    $scope.item = item;

    $scope.share = function(){console.log('share')};

    $scope.close = function () {
      $modalInstance.close();
    };
  }
);