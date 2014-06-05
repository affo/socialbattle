angular.module('character', ['restangular'])

.controller('CharacterDetail',
  ['$scope', '$stateParams', 'Restangular', '$state', '$localStorage',
  function($scope, $stateParams, Restangular, $state, $localStorage){
    $scope.endpoint = Restangular.one('characters', $stateParams.name);
    $scope.is_me = false;
    $scope.load_character = function(){
      $scope.endpoint.get()
      .then(
        function(character){
          $scope.character = character;
          if(character.name == $localStorage.character){
            $scope.is_me = true;
          }
        }
      );
    };

    $scope.load_character();
  }
  ]
)

.controller('CharacterAbilities',
  ['$scope', '$stateParams', 'Restangular', '$state', '$localStorage',
  function($scope, $stateParams, Restangular, $state, $localStorage){
    $scope.endpoint.getList('abilities').then(
      function(abilities){
        $scope.abilities = abilities;
      }
    );

    $scope.endpoint.getList('abilities/next').then(
      function(abilities){
        $scope.next_abilities = abilities;
      }
    );

    $scope.use_ability = function(ability){
      var data = {
        ability: ability.url,
      };

      $scope.endpoint.all('use_ability').post(data)
      .then(
        function(response){
          $scope.load_character();  
        },
        function(response){
          $scope.alert = {type: 'danger', msg: response.data.msg};
        }
      );

    };

    $scope.learn_ability = function(ability){
      var data = {
        ability: ability.url,
      };

      $scope.endpoint.all('abilities/next').post(data)
      .then(
        function(response){
          $scope.abilities.push(ability);
          $scope.character.ap -= ability.ap_required;
          //update next abilities
          $scope.next_abilities = $scope.endpoint.getList('abilities/next').$object;
        },
        function(response){
          $scope.alert = {type: 'danger', msg: response.data.msg};
        }
      );
    };

    $scope.alert = undefined;
    $scope.close_alert = function(){
      $scope.alert = undefined;
    };

  }
  ]
)

.controller('CharacterInventory',
  ['$scope', '$stateParams', 'Restangular', '$state', '$localStorage',
  function($scope, $stateParams, Restangular, $state, $localStorage){
    $scope.endpoint.getList('inventory').then(
      function(inventory){
        $scope.inventory = inventory;
      }
    );

    $scope.endpoint.one('weapon').get().then(
      function(eq_weapon){
        $scope.eq_weapon = eq_weapon;

        $scope.endpoint.getList('weapons').then(
          function(weapons){
            for(var i = 0; i < weapons.length; i++){
              if(weapons[i].equipped){
                weapons.splice(i, 1);
                break;
              }
            }
            $scope.weapon_records = weapons;
          }
        );
      }
    );

    $scope.endpoint.one('armor').get().then(
      function(eq_armor){
        $scope.eq_armor = eq_armor;

        $scope.endpoint.getList('armors').then(
          function(armors){
            for(var i = 0; i < armors.length; i++){
              if(armors[i].equipped){
                armors.splice(i, 1);
                break;
              }
            }
            $scope.armor_records = armors;
          }
        );
      }
    );

    $scope.equip_weapon = function(record){
      var rec = Restangular.oneUrl('inventory', record.url);
      rec.equipped = true;
      rec.put().then(
        function(response){
          $scope.weapon_records.push($scope.eq_weapon);
          for(var i = 0; i < $scope.weapon_records.length; i++){
            if($scope.weapon_records[i].url == response.url){
              $scope.weapon_records.splice(i, 1);
              break;
            }
          }
          $scope.eq_weapon = response;
          $scope.load_character();
        }
      );
    };

    $scope.equip_armor = function(record){
      var rec = Restangular.oneUrl('inventory', record.url);
      rec.equipped = true;
      rec.put().then(
        function(response){
          $scope.armor_records.push($scope.eq_armor);
          for(var i = 0; i < $scope.armor_records.length; i++){
            if($scope.armor_records[i].url == response.url){
              $scope.armor_records.splice(i, 1);
              break;
            }
          }
          $scope.eq_armor = response;
          $scope.load_character();
        }
      );
    };

    $scope.use_item = function(record){
      console.log(record.item.url);
      var data = {
        item: record.item.url,
      };

      $scope.endpoint.all('use_item').post(data)
      .then(
        function(response){
          $scope.character.curr_hp = response.curr_hp;
          record.quantity--;
        },
        function(response){
          $scope.alert = {type: 'danger', msg: response.data.msg};
        }
      );
    };

    $scope.alert = undefined;
    $scope.close_alert = function(){
      $scope.alert = undefined;
    };

  }
  ]
);