'use strict';

/* Services */

angular.module('services', [])

.factory('SpawnService',
  function($q, $timeout, Restangular){
    var factory = {};
    var TIMEOUT_RANGE = [5, 10].map(function(x){ return x * 1000;}); //timeout range in ms

    //returns a promise containing a mob
    factory.spawn = function(mobs){
      if(mobs.length == 0) return {};
      var deferred = $q.defer();
      //randomly selected mob
      var mob = mobs[Math.floor(Math.random()*mobs.length)];

      var timeout = Math.floor(TIMEOUT_RANGE[0] + Math.random()*(TIMEOUT_RANGE[1] - TIMEOUT_RANGE[0]));
      console.log('TO: ' + timeout);

      $timeout(function(){
        if(mob){
          mob.max_hp = mob.hp;
          delete mob.hp;
          mob.curr_hp = mob.max_hp;
          deferred.resolve(mob);
        } else {
          deferred.reject('No mob found');
        }
      }, timeout, true);

      return deferred.promise;
    };

    return factory;
  }
)

.factory('AttackService',
  function($q, $timeout, Restangular){
    var factory = {};
    
    //attacks using the endpoint which could be:
    // - /characters/{character_name}/use_ability
    // - /mobs/{mob_slug}/use_ability
    //the attacked_id and the ability.
    //returns a promise of the result of the attack, which, in turn, contains
    // - the charge time
    // - the promise of the damage, postponed by the ct
    factory.attack = function(endpoint, attacked_id, ability){
      var deferred = $q.defer();
      var data = {
        attacked: attacked_id,
        ability: ability.url,
      };
      if(!attacked_id){
        delete data.attacked;
      }

      endpoint.post(data)
      .then(
        function(response){
          var attack = $q.defer();
          var r = {
            ct: response.ct,
            dmg: response.dmg,
          }

          $timeout(function(){
            attack.resolve(
              {
                ability: ability,
                dmg: r.dmg,
              }
            );
          }, r.ct, true);

          deferred.resolve({ct: r.ct, attack: attack.promise});
        }
      );
      return deferred.promise;
    };

    return factory;
  }
)

.factory('MobService',
  function(Restangular, AttackService){
    var factory = {};

    factory.attack = function(mob_slug, character_url, abilities){
      var ability = abilities[Math.floor(Math.random()*abilities.length)];
      var attacked_id = character_url;
      if(ability.element == 'H'){ // white magic
        attacked_id = undefined;
      }
      var endpoint = Restangular.one('mobs', mob_slug).all('use_ability');
      return AttackService.attack(endpoint, attacked_id, ability);
    }

    return factory;
  }
)

.factory('CharacterService',
  function(Restangular, AttackService){
    var factory = {};

    factory.attack = function(character_name, target, ability){
      var endpoint = Restangular.one('characters', character_name).all('use_ability');
      var attacked_id = target;
      return AttackService.attack(endpoint, attacked_id, ability);
    };

    factory.use_item = function(item){
      var data = {item: item.url};
      return Restangular.one('characters', character_name).all('use_item').post(data);
    };

    return factory;
  }
);