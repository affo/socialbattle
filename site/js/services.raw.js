'use strict';

/* Services */

angular.module('services', [])

.factory('SpawnService',
  function($q, $timeout, Restangular){
    var factory = {};
    var TIMEOUT_RANGE = [5, 10].map(function(x){ return x * 1000;}); //timeout range in ms
    var timeout_promise;
    var deferred;

    //returns a promise containing a mob
    factory.spawn = function(mobs){
      if(mobs.length == 0) return {};
      deferred = $q.defer();
      //randomly selected mob
      var obj = mobs[Math.floor(Math.random()*mobs.length)];
      //cloning the mob as suggested by
      //http://stackoverflow.com/questions/122102/what-is-the-most-efficient-way-to-clone-an-object/5344074#5344074
      var mob = JSON.parse(JSON.stringify(obj));

      var timeout = Math.floor(TIMEOUT_RANGE[0] + Math.random()*(TIMEOUT_RANGE[1] - TIMEOUT_RANGE[0]));
      //console.log('TO: ' + timeout);

      timeout_promise = $timeout(function(){
        mob.max_hp = mob.hp;
        mob.curr_hp = mob.hp;
        delete mob.hp;
        deferred.resolve(mob);
      }, timeout, true);

      return deferred.promise;
    };

    factory.stop = function(){
      if(timeout_promise){
        $timeout.cancel(timeout_promise);
        deferred.reject('Stopped');
      }
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
          var ct = response.ct * 1000; //it comes in seconds from the server
          var dmg = response.dmg;

          $timeout(function(){
            attack.resolve(
              {
                ability: ability,
                attacked_hp: response.attacked_hp,
                attacker_mp: response.attacker_mp,
                dmg: dmg,
              }
            );
          }, ct, true);

          deferred.resolve({ct: ct, attack: attack.promise});
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

    factory.attack = function(character, target, ability){
      var endpoint = Restangular.one('characters', character.name).all('use_ability');
      var attacked_id = target;
      if(character.url == target){
        attacked_id = undefined;
      }
      return AttackService.attack(endpoint, attacked_id, ability);
    };

    factory.use_item = function(character_name, item){
      var data = {item: item.url};
      return Restangular.one('characters', character_name).all('use_item').post(data);
    };

    return factory;
  }
)

.factory('FBStoriesService',
  function(Facebook, $localStorage){
    var factory = {};

    //@ifndef HEROKU
    factory.APP_NAMESPACE = 'socialbattle_test';
    //@endif

    //@ifdef HEROKU
    factory.APP_NAMESPACE = 'socialbattlegame';
    //@endif

    factory.defeat = function(character, room, mob){
      if(!$localStorage.facebook) return;

      var fb_data = {
        character: character,
        room: room,
        mob: mob,
      };

      Facebook.api('me/' + factory.APP_NAMESPACE +':defeat', 'post', fb_data,
        function(response){
          if(response.error){
            console.log(response.error);
          }else{
            console.info('Story added to activity log');
          }
        });
    };

    factory.lose = function(character, room, mob){
      if(!$localStorage.facebook) return;

      var fb_data = {
        character: character,
        room: room,
        mob: mob,
      };

      Facebook.api('me/' + factory.APP_NAMESPACE +':lose_against', 'post', fb_data,
        function(response){
          if(response.error){
            console.log(response.error);
          }else{
            console.info('Story added to activity log');
          }
        });
    };

    factory.buy = function(character, room, item){
      if(!$localStorage.facebook) return;

      var fb_data = {
        character: character,
        room: room,
        loot: item,
      };

      Facebook.api('me/' + factory.APP_NAMESPACE +':buy', 'post', fb_data,
        function(response){
          if(response.error){
            console.log(response.error);
          }else{
            console.info('Story added to activity log');
          }
        });
    };

    factory.sell = function(character, room, item){
      if(!$localStorage.facebook) return;

      var fb_data = {
        character: character,
        room: room,
        loot: item,
      };

      Facebook.api('me/' + factory.APP_NAMESPACE +':buy', 'post', fb_data,
        function(response){
          if(response.error){
            console.log(response.error);
          }else{
            console.info('Story added to activity log');
          }
        });
    };

    return factory;
  }
);