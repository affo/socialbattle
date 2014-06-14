angular.module('room', ['luegg.directives'])

.controller('Rooms',
  ['$scope', '$state', '$localStorage', 'Restangular', 
  function($scope, $state, $localStorage, Restangular){
    $scope.pverooms = Restangular.all('rooms/pve').getList().$object;
    $scope.relaxrooms = Restangular.all('rooms/relax').getList().$object;
  }
  ]
)

.controller('PVERoom',
  ['$scope', 'Restangular', '$stateParams', '$localStorage', '$modal', 'Facebook',
    'SpawnService', 'MobService', 'CharacterService', 'FBStoriesService',
    'character', 'character_abilities', 'weapons', 'armors', 'items',
    'mobs', 'room', '$timeout', '$state', '$rootScope',
  function($scope, Restangular, $stateParams, $localStorage, $modal, Facebook,
            SpawnService, MobService, CharacterService, FBStoriesService,
            character, character_abilities, weapons, armors, items,
            mobs, room, $timeout, $state, $rootScope){

    if(character.curr_hp <= 0){
      var m = $modal.open({
        templateUrl: 'deadModal.html',
        controller: 'DeadModal',
        backdrop: 'static',
        keyboard: false,
        resolve: {
          character: function(){
            return character.name;
          },
        }
      });
    }

    var TIMEOUT_RANGE = [5, 10].map(function(x){ return x * 1000;}); //timeout range in ms
    var atb_active = false;
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

    var mob_promise;

    $scope.$on('$destroy', function(){
      SpawnService.stop();
      console.info('spawn stopped');
    });

    $rootScope.$on('$stateChangeStart', 
      function(event, toState, toParams, fromState, fromParams){
        if(mob_promise){
          event.preventDefault(); // stop transition
          //open modal
          var m = $modal.open({
            templateUrl: 'flightModal.html',
            controller: 'FlightModal',
          });

          m.result.then(
            function(stay){
              // if flight, then go
              if(!stay){
                console.info('mob stopped');
                $timeout.cancel(mob_promise);
                mob_promise = undefined;
                $state.go(toState, toParams);
              }
            }
          );

        }    
      }
    );



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
    };

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
            backdrop: 'static',
            keyboard: false,
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
        },

        function(response){ //stopped
          console.log($scope.room.name + ': ' + response);
        }
      );
    };

    var mob_ai = function(abilities, ct){
      if($scope.mob.curr_hp === 0 || !is_character_alive()){ //if the battle id ended, the mob stops
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

                //if the character is dead
                if(!is_character_alive()){
                  end_battle(false);
                  return;
                }
                mob_promise = mob_ai(abilities, response.ct); //recursive call
              }
            );
          }
        );
      }, timeout, true);
    };

    var end_battle = function(win){
      if(!$scope.fighting) return;

      if(mob_promise){
        console.info('mob stopped');
        $timeout.cancel(mob_promise);
        mob_promise = undefined;
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
                  character: function(){
                    return $scope.character;
                  },

                  mob: function(){
                    return $scope.mob;
                  },

                  room: function(){
                    return $scope.room;
                  },

                  end: function(){
                    return response;
                  },
                }
              });

            m.result.then(
              function(){
                //re-resolve
                $scope.weapons = Restangular.one('characters', $localStorage.character).getList('weapons').$object;
                $scope.armors = Restangular.one('characters', $localStorage.character).getList('armors').$object;
                $scope.items = Restangular.one('characters', $localStorage.character).getList('items').$object;
                Restangular.one('characters', $localStorage.character).get().then(
                  function(response){
                    $scope.character = Restangular.stripRestangular(response);
                    //re-spawn
                    if(is_character_alive()){
                      spawn();
                    }
                  }
                );
              }
            );
          }
        );

        //send activity to facebook
        FBStoriesService.defeat($scope.character.fb_id, $scope.room.fb_id, $scope.mob.fb_id);
      }else{
        //send activity to facebook
        FBStoriesService.lose($scope.character.fb_id, $scope.room.fb_id, $scope.mob.fb_id);

        var m = $modal.open({
            templateUrl: 'loseModal.html',
            controller: 'LoseModal',
            backdrop: 'static',
            keyboard: false,
            resolve: {
              character: function(){
                return $scope.character;
              },

              room: function(){
                return $scope.room;
              },

              mob: function(){
                return $scope.mob;
              },
            }
          });
      }
    };

    var is_character_alive = function(){
      return $scope.character.curr_hp > 0;
    };

    var MAX = 100;
    var FACTOR = 4;
    $scope.max = MAX;
    $scope.progr = 0;
    var atb_bar = function(time){
      console.log('CT ' + time);
      atb_active = true;
      //if the time is too short only charge the bar and descharge
      if(time < 1500){
        $scope.progr = MAX;
        $timeout(function(){
          $scope.progr = 0;
          atb_active = false;
        }, 1500, true);
        
        return;
      }


      var slice = (time - 500) / FACTOR;

      var rec = function(slice, i){
        if(i > FACTOR + 1){
          $scope.progr = 0;
          atb_active = false;
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
      if(atb_active) return; // another attack is on
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
              var hp = response.attacked_hp;
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
              if($scope.mob.curr_hp === 0){
                end_battle(true);
              }

              //lose
              if($scope.character.curr_hp === 0){
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
    if(is_character_alive()) spawn();
  }
  ]
)

.controller('SpawnModal',
  ['$scope', '$modalInstance', 'room', 'mob',
  function($scope, $modalInstance, room, mob){
    $scope.room = room;
    $scope.mob = mob;

    $scope.start_fight = function(){
      $modalInstance.close();
    };
  }
  ]
)

.controller('WinModal',
  ['$scope', '$modalInstance', '$localStorage',
    'Facebook', 'FBStoriesService', 'Restangular',
    'character', 'room', 'mob', 'end',
  function($scope, $modalInstance, $localStorage,
            Facebook, FBStoriesService, Restangular,
            character, room, mob, end){
    $scope.mob = mob.name;
    $scope.end = end;
    $scope.alerts = [];

    $scope.tweet_text = 'Won a battle against ' + mob.name;

    $scope.share = function(){
      console.log('share');
      //disable share button
      angular.element('#share-fb-button').addClass('disabled');
      
      var msg = 'Won a battle against ' + mob;
      Facebook.getLoginStatus(
        function(response){
          $scope.$apply(function(){
            if(response.status == 'connected'){
              //ok
              //associate with facebook
              var data = {access_token: response.authResponse.accessToken};
              Restangular.all('sa/associate/').customGET('facebook', data)
              .then(
                function(user){
                  $localStorage.user = user.username;
                  $localStorage.facebook = true;

                  var fb_data = {
                    character: character.fb_id,
                    room: room.fb_id,
                    mob: mob.fb_id,
                  };

                  Facebook.ui({
                    method: 'share_open_graph',
                    action_type: FBStoriesService.APP_NAMESPACE + ':defeat',
                    action_properties: JSON.stringify(fb_data),
                  },
                    function(response) {
                      if(!response || response.error){
                        $scope.alerts.push({type: 'danger', msg: response.error});
                      } else {
                        $scope.alerts.push({type: 'success', msg: 'Succesfully posted to your timeline'});
                        console.log(response);
                      }
                    }
                  );
                },
                function(response){
                  //error
                  console.log(response);
                }
              );
            }else if(response.status === 'not_authorized'){
              // The person is logged into Facebook, but not your app.
              // and so I'm very sorry...
              console.log(response);
            } else {
              // The person is not logged into Facebook, so we're not sure if
              // they are logged into this app or not.
              // let's make him log in to Facebook
              Facebook.login(function(response){
                if(response.authResponse){
                  $scope.share();
                }else{
                  //the user stopped the auth
                }
              }, {scope: 'publish_actions'});
            }
          }); //$scope.$apply
        }
      );
    };

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };

    $scope.close = function(){
      $modalInstance.close();
    };
  }
  ]
)

.controller('LoseModal',
  ['$scope', '$modalInstance', '$state', '$localStorage',
    'Facebook', 'FBStoriesService', 'Restangular',
    'character', 'room', 'mob',
  function($scope, $modalInstance, $state, $localStorage,
              Facebook, FBStoriesService, Restangular,
              character, room, mob){
    $scope.mob = mob.name;
    $scope.alerts = [];

    var redirect = function(){
      $state.go('character.inventory', {name: $localStorage.character});
    };

    $scope.tweet_text = 'Lose a battle against ' + mob.name;

    $scope.share = function(){
      console.log('share');
      //disable share button
      angular.element('#share-fb-button').addClass('disabled');

      var msg = 'Lose a battle against ' + mob;
      Facebook.getLoginStatus(
        function(response){
          $scope.$apply(function(){
            if(response.status == 'connected'){
              //ok
              //associate with facebook
              var data = {access_token: response.authResponse.accessToken};
              Restangular.all('sa/associate/').customGET('facebook', data)
              .then(
                function(user){
                  $localStorage.user = user.username;
                  $localStorage.facebook = true;

                  var fb_data = {
                    character: character.fb_id,
                    room: room.fb_id,
                    mob: mob.fb_id,
                  };

                  Facebook.ui({
                    method: 'share_open_graph',
                    action_type: FBStoriesService.APP_NAMESPACE + ':lose_against',
                    action_properties: JSON.stringify(fb_data),
                  },
                    function(response) {
                      if(!response || response.error){
                        $scope.alerts.push({type: 'danger', msg: response.error});
                      } else {
                        $scope.alerts.push({type: 'success', msg: 'Succesfully posted to your timeline'});
                        console.log(response);
                      }
                    }
                  );
                },
                function(response){
                  //error
                  console.log(response);
                }
              );
            }else if(response.status === 'not_authorized'){
              // The person is logged into Facebook, but not your app.
              // and so I'm very sorry...
            } else {
              // The person is not logged into Facebook, so we're not sure if
              // they are logged into this app or not.
              // let's make him log in to Facebook
              Facebook.login(function(response){
                if(response.authResponse){
                  $scope.share();
                }else{
                  //the user stopped the auth
                }
              }, {scope: 'publish_actions'});
            }
          }); //$scope.$apply
        }
      );
    };

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };

    $scope.close = function(){
      $modalInstance.close();
      redirect();
    };
  }
  ]
)

.controller('FlightModal',
  ['$scope', '$modalInstance',
  function($scope, $modalInstance){
    $scope.flight = function(){
      $modalInstance.close(false);
    };

    $scope.close = function(){
      $modalInstance.close(true);
    };
  }
  ]
)

.controller('DeadModal',
  ['$scope', '$modalInstance', '$state', 'FBStoriesService', 'character',
  function($scope, $modalInstance, $state, FBStoriesService, character){
    $scope.close = function(){
      $modalInstance.close();
      $state.go('character.inventory', {name: character});
    };
  }
  ]
)

.controller('RelaxRoom',
  ['$scope', 'Restangular', '$stateParams', '$localStorage', '$modal',
    'Facebook', 'FBStoriesService',
    'character', 'room',
  function($scope, Restangular, $stateParams, $localStorage, $modal,
            Facebook, FBStoriesService,
            character, room){
    $scope.endpoint = Restangular.one('rooms/relax', $stateParams.room_name);
    $scope.character_endpoint = Restangular.one('characters', $localStorage.character.name);
    $scope.character = $scope.character_endpoint.get().$object;
    $scope.init_msg = 'Welcome, I am the merchant at ' + $stateParams.room_name;
    $scope.buy_items = $scope.endpoint.all('items').getList().$object;
    $scope.sell_items = $scope.character_endpoint.getList('inventory').$object;
    $scope.msgForm = {};
    $scope.action = 'BUY';

    $scope.toggle_action = function(){
      if($scope.action == 'BUY'){
        $scope.action = 'SELL';
      }else{
        $scope.action = 'BUY';
      }
      ai.reset();
    };

    var ai = {
      find_item: function(item_name){
        //find the item by name
        var i;
        if($scope.action == 'BUY'){
          for(i = 0; i < $scope.buy_items.length; i++){
            if(item_name == $scope.buy_items[i].name){
              return $scope.buy_items[i];
            }
          }
          return undefined;
        }else if($scope.action == 'SELL'){
          for(i = 0; i < $scope.sell_items.length; i++){
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
        var msg;

        if(item){
          $scope.selected_item = item;
          msg = {
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
          msg = {
            content: content,
            info: true,
          };
          $scope.messages.push(msg);
        }
      },

      HOW_MANY: function(quantity){
        var msg;
        if(isNaN(quantity)){
          msg = {
            content: 'Please give me a valid number',
            info: true,
          };
          $scope.messages.push(msg);
        }else{
          msg = {
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

        $scope.sell_items = $scope.character_endpoint.getList('inventory').$object;
      },

      KO: function(resp){
        var msg = {
            content: resp.data.msg,
            from_merchant: true,
        };
        $scope.messages.push(msg);
        ai.reset();
      },
    };

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
      var msg = $scope.msgForm.content;
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
      //send activity to facebook
      if($scope.action == 'BUY'){
        FBStoriesService.buy(character.fb_id, room.fb_id, $scope.selected_item.fb_id);
      }else{
        FBStoriesService.sell(character.fb_id, room.fb_id, $scope.selected_item.fb_id);
      }

      var modalInstance = $modal.open({
        templateUrl: 'transactionModal.html',
        controller: 'TransactionModal',
        resolve: {
          user: function (){
            return $localStorage.user;
          },

          character: function(){
            return character;
          },

          item: function(){
            return $scope.selected_item;
          },

          shop: function(){
            return room;
          },

          action: function(){
            if($scope.action == 'BUY'){
              return 'bought';
            }
            return 'sold';
          },

          fb_action: function(){
            return $scope.action.toLowerCase();
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
  }
  ]
)

.controller('TransactionModal',
  ['$scope', '$modalInstance', 'Restangular', '$localStorage',
    'Facebook', 'FBStoriesService',
    'user', 'action', 'character',
    'shop', 'item', 'fb_action',
  function($scope, $modalInstance, Restangular, $localStorage,
              Facebook, FBStoriesService,
              user, action, character,
              shop, item, fb_action){
    $scope.user = user;
    $scope.action = action;
    $scope.character = character.name;
    $scope.shop = shop.name;
    $scope.item = item.name;
    $scope.alerts = [];

    $scope.share = function(){
      console.log('share');
      var msg = user + '#' + character + ' bought some ' + item + ' @' + shop;
      Facebook.getLoginStatus(
        function(response){
          $scope.$apply(function(){
            if(response.status == 'connected'){
              //ok
              //associate with facebook
              var data = {access_token: response.authResponse.accessToken};
              Restangular.all('sa/associate/').customGET('facebook', data)
              .then(
                function(user){
                  $localStorage.user = user.username;
                  $localStorage.facebook = true;

                  var fb_data = {
                    character: character.fb_id,
                    room: shop.fb_id,
                    loot: item.fb_id,
                  };

                  Facebook.ui({
                    method: 'share_open_graph',
                    action_type: FBStoriesService.APP_NAMESPACE + ':' + fb_action,
                    action_properties: JSON.stringify(fb_data),
                  },
                    function(response) {
                      if(!response || response.error){
                        $scope.alerts.push({type: 'danger', msg: response.error});
                      } else {
                        $scope.alerts.push({type: 'success', msg: 'Succesfully posted to your timeline'});
                        console.log(response);
                      }
                    }
                  );
                },
                function(response){
                  //error
                  console.log(response);
                }
              );
            }else if(response.status === 'not_authorized'){
              // The person is logged into Facebook, but not your app.
              // and so I'm very sorry...
            } else {
              // The person is not logged into Facebook, so we're not sure if
              // they are logged into this app or not.
              // let's make him log in to Facebook
              Facebook.login(function(response){
                if(response.authResponse){
                  $scope.share();
                }else{
                  //the user stopped the auth
                }
              }, {scope: 'publish_actions'});
            }
          }); //$scope.$apply
        }
      );
    };

    $scope.tweet_text = $scope.user + ' using ' + $scope.character + ' bought some ' + $scope.item + ' @ ' + $scope.shop;

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };

    $scope.close = function () {
      $modalInstance.close();
    };
  }
  ]
);