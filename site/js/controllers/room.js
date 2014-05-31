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
  function($scope, Restangular, $stateParams, $localStorage, $modal, SpawnService, MobService, CharacterService,
            character, character_abilities, weapons, armors, items,
            mobs, room, $timeout, $state){

    var TIMEOUT_RANGE = [5, 10].map(function(x){ return x * 1000;}); //timeout range in ms
    $scope.messages = [];
    $scope.fighting = false;
    $scope.action = 'ABILITY';
    $scope.abilityForm = {};
    $scope.itemForm = {};
    $scope.target = undefined;

    $scope.character = character;
    $scope.abilities = character_abilities;
    $scope.weapons = weapons;
    $scope.armors = armors;
    $scope.armors = armors;
    $scope.items = items;
    $scope.room = room;

    var spawn_promise = undefined;
    var mob_promise = undefined;

    $scope.$on('$destroy', function(){
      if(mob_promise){
        console.info('mob stopped');
        $timeout.cancel(mob_promise);
      }

      if(spawn_promise){
        console.info('spawn stopped');
        $timeout.cancel(spawn_promise);
      }
    });



    var push_mob = function(attacker, attacked, ability, dmg){
      var data = {
        attacked: attacked,
        attacker: attacker,
        ability: ability,
        dmg: dmg,
        from_mob: true,
      };
      $scope.messages.push(data);
    };

    var push_character = function(attacker, attacked, ability, dmg){
      var data = {
        attacked: attacked,
        attacker: attacker,
        ability: ability,
        dmg: dmg,
        from_character: true,
      };
      $scope.messages.push(data);
    };

    var push_info = function(msg){
      var data = {
        content: msg,
        info: true,
      };
      $scope.messages.push(data);
    };

    var find_item = function(item_name){
      //find the item by name
      for(var i = 0; i < $scope.items.length; i++){
        if(item_name == $scope.items[i].item.name){
          return $scope.items[i];
        }
      }
      return undefined;
    };

    var find_ability = function(ability_name){
      //find the ability by name
      for(var i = 0; i < $scope.abilities.length; i++){
        if(ability_name == $scope.abilities[i].name){
          return $scope.abilities[i];
        }
      }
      return undefined;
    };

    $scope.toggle_action = function(){
      if($scope.action == 'ABILITY'){
        $scope.action = 'ITEM';
      }else{
        $scope.action = 'ABILITY';
      }
    };

    $scope.filter_mob_msg = function(msg){
      console.log(msg);
      if(msg.from_mob) return false;
      return true;
    };

    $scope.filter_character_msg = function(msg){
      console.log(msg);
      if(msg.from_character) return false;
      return true;
    };

    $scope.swap_target = function(){
      if($scope.target == $scope.mob){
        $scope.target = $scope.character;
      }else{
        $scope.target = $scope.mob;
      }
    }

    $scope.equip = function(item, is_weapon){
      if(item.equipped){ //already equipped
        return;
      }
      var rec = Restangular.oneUrl('inventory', item.url);
      rec.equipped = true;
      rec.put().then(
        function(response){
          var iter = armors;
          if(is_weapon){
            iter = weapons;
          }

          for(var i = 0; i < iter.length; i++){
            if(iter[i].equipped){
              iter[i].equipped = false;
            }
          }

          item.equipped = true;
        }
      );
    };

    var spawn = function(){
      return SpawnService.spawn(mobs).then(
        function(mob){
          //start modal
          var m = $modal.open({
            templateUrl: 'spawnModal.html',
            controller: 'SpawnModal',
            resolve: {
              room: function () {
                return $scope.room.name;
              },

              mob: function () {
                return mob.name;
              },
            }
          });

          m.result.then(
            function(){
              $scope.mob = mob;
              Restangular.one('mobs', mob.slug).getList('abilities')
              .then(
                function(response){
                  var abilities = Restangular.stripRestangular(response);
                  $scope.fighting = true;
                  $scope.target = mob;
                  // START MOB
                  mob_promise = mob_ai(abilities, 0);
                }
              );
            }
          );
        }
      );
    };

    var mob_ai = function(abilities, ct){
      if($scope.mob.curr_hp == 0 || !is_character_alive()){ //if the battle id ended, the mob stops
          return;
      }

      var timeout = Math.floor(TIMEOUT_RANGE[0] + Math.random()*(TIMEOUT_RANGE[1] - TIMEOUT_RANGE[0])) + ct;
      //console.log('Next attack in: ' + timeout);

      return $timeout(function(){
        MobService.attack($scope.mob.slug, $scope.character.url, abilities)
        .then(
          function(response){
            response.attack.then(
              function(attack){
                var target = $scope.character.name;
                var dmg = attack.dmg;
                var hp = attack.attacked_hp;
                if(attack.ability.element == "H"){ //white magic
                  target = $scope.mob.name;
                  hp = $scope.mob.curr_hp - dmg;
                  if(hp > $scope.mob.max_hp) hp = $scope.mob.max_hp;
                }else{
                  $scope.character.curr_hp = hp;
                }

                push_mob($scope.mob.name, target, attack.ability.name, attack.dmg);
                mob_promise = mob_ai(abilities, response.ct); //recursive call
              }
            );
          }
        );
      }, timeout, true);
    };

    var end_battle = function(win){
      if(mob_promise){
        console.info('mob stopped');
        $timeout.cancel(mob_promise);
      }
      $scope.fighting = false;
      push_info('Battle ended');

      if(win){
        Restangular.oneUrl('character', character.url)
        .all('end_battle').post({mob: $scope.mob.url})
        .then(
          function(response){
            var m = $modal.open({
                templateUrl: 'winModal.html',
                controller: 'WinModal',
                resolve: {
                  mob: function () {
                    return $scope.mob.name;
                  },

                  end: function(){
                    return response;
                  },
                }
              });

            m.result.then(
              function(){
                if(is_character_alive()) spawn_promise = spawn();
              }
            );
          }
        );
      }else{
        var m = $modal.open({
            templateUrl: 'loseModal.html',
            controller: 'LoseModal',
            resolve: {
              mob: function(){
                return $scope.mob.name;
              },
            }
          });
      }
    };

    var is_character_alive = function(){
      return $scope.character.curr_hp > 0;
    };

    var MAX = 100;
    var FACTOR = 32;
    $scope.max = MAX;
    $scope.progr = 0;
    var atb_bar = function(time){
      console.log('CT ' + time);
      //if the time is too short only charge the bar and descharge
      if(time < 1500){
        $scope.progr = MAX;
        $timeout(function(){
          $scope.progr = 0;
        }, 1500, true)
        
        return;
      }


      var slice = (time - 500) / FACTOR;

      var rec = function(slice, i){
        if(i > FACTOR + 1){
          $scope.progr = 0;
          return;
        }

        $timeout(function(){
          $scope.progr = MAX * (i / FACTOR);
        }, slice, true)
        .then(
          function(){
            rec(slice, i + 1);
          }
        );
      };

      rec(slice, 1);

    };

    $scope.attack = function(){
      var target_url = $scope.target.url;
      var ability = find_ability($scope.abilityForm.ability);
      $scope.abilityForm = {};
      if(!ability){
        push_info('Ability not found');
        return;
      }

      CharacterService.attack($scope.character, target_url, ability)
      .then(
        function(response){
          var ct = response.ct; //use charge time
          atb_bar(ct); //handles atb bar
          response.attack.then(
            function(response){
              //now we have the dmg to display
              var dmg = response.dmg;
              var ability = response.ability;
              var hp = response.attacked_hp
              var mp = response.attacker_mp;

              if(!hp){
                hp = $scope.target.curr_hp - dmg;
                if(hp < 0) hp = 0;
              }
             
              //apply attack
              $scope.target.curr_hp = hp;
              $scope.character.curr_mp = mp;

              push_character($scope.character.name, $scope.target.name, ability.name, dmg);

              //win
              if($scope.mob.curr_hp == 0){
                end_battle(true);
              }

              //lose
              if($scope.character.curr_hp == 0){
                end_battle(false);
              }
            }
          );
        },

        function(response){
          console.log(response);
          push_info(response.data.msg);
        }
      );
    };

    $scope.use_item = function(){
      var item = find_item($scope.itemForm.item);
      $scope.itemForm = {};
      if(!item){
        push_info('Item not found');
        return;
      }
      CharacterService.use_item($scope.character.name, item.item).then(
        function(response){
          $scope.character.curr_hp = response.curr_hp;
          item.quantity -= 1;
        },
        function(response){
          push_info(response.data.msg);
        }
      );
    };

    ///////////START SPAWNING
    spawn_promise = spawn();
})

.controller('SpawnModal',
  function($scope, $modalInstance, room, mob){
    $scope.room = room;
    $scope.mob = mob;

    $scope.start_fight = function(){
      $modalInstance.close();
    };
  }
)

.controller('WinModal',
  function($scope, $modalInstance, mob, end){
    $scope.mob = mob;
    $scope.end = end;

    $scope.share = function(){};

    $scope.close = function(){
      $modalInstance.close();
    };
  }
)

.controller('LoseModal',
  function($scope, $modalInstance, $state, $localStorage, mob){
    var redirect = function(){
      $state.go('character.inventory', {name: $localStorage.character});
    };

    $scope.share = function(){
      redirect();
    };

    $scope.close = function(){
      $modalInstance.close();
      redirect();
    };
  }
)

.controller('FlightModal',
  function($scope, $modalInstance){
    $scope.flight = function(){};

    $scope.close = function(){
      $modalInstance.close();
    };
  }
)

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