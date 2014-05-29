angular.module('states', ['ui.router'])

.config(

	function($stateProvider){
		$stateProvider

    .state('unlogged', {
      url: '/',
      templateUrl: 'html/home.html',
      controller: 'Auth',
    })

    .state('logged', {
      templateUrl: 'html/layout.html',
    })

    .state('user', {
      parent: 'logged',

      url: '/users/:username',
      templateUrl: 'html/partials/user.html',
      controller: 'UserDetail'
    })

      .state('user.following', {
        url: '/following',
        templateUrl: 'html/partials/user.followx.html',
        controller: 'UserFollowing'
      })

      .state('user.followers', {
        url: '/followers',
        templateUrl: 'html/partials/user.followx.html',
        controller: 'UserFollowers'
      })

      .state('user.posts', {
        url: '/posts',
        templateUrl: 'html/partials/posts.html',
        controller: 'UserPosts'
      })

      .state('user.characters', {
        url: '/characters',
        templateUrl: 'html/partials/user.characters.html',
        controller: 'UserCharacters'
      })

    .state('pveroom', {
      parent: 'logged',

      url: '/rooms/:room_name',
      templateUrl: 'html/partials/pveroom.html',

      resolve: {
        character: function($localStorage, Restangular){
          console.log('RESOLVING');
          return Restangular.all('characters', $localStorage.character).get()
          .then(
            function(response){
              var obj = Restangular.stripRestangular(reponse);
              return obj;
            },
            function(response){
              console.log(response);
            }
          );
        },

        character_abilities: function($localStorage, Restangular){
          console.log('RESOLVING');
          return Restangular.all('characters', $localStorage.character).getList('abilities')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(reponse);
              return obj;
            }
          );
        },

        character_inventory: function($localStorage, Restangular){
          return Restangular.all('characters', $localStorage.character).getList('inventory')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(reponse);
              return obj;
            }
          );
        },

        mobs: function($stateParams, Restangular){
          return Restangular.one('rooms/pve', $stateParams.room_name).getList('mobs')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(reponse);
              return obj;
            }
          );
        },

        room: function($stateParams, Restangular){
          return Restangular.one('rooms/pve', $stateParams.room_name).get()
          .then(
            function(response){
              var obj = Restangular.stripRestangular(reponse);
              return obj;
            }
          );
        },
      },

      controller: 'PVERoom',
    }
    )

    .state('relaxroom', {
      parent: 'logged',

      url: '/rooms/:room_name',
      templateUrl: 'html/partials/relaxroom.html',
      controller: 'RelaxRoom'
    })

      .state('relaxroom.posts', {
        url: '/posts',
        templateUrl: 'html/partials/posts.html',
        controller: 'RelaxRoomPosts'
      })

    .state('character', {
      parent: 'logged',

      url: '/characters/:name',
      templateUrl: 'html/partials/character.html',
      controller: 'CharacterDetail'
    })

      .state('character.abilities', {
        url: '/abilities',
        templateUrl: 'html/partials/character.abilities.html',
        controller: 'CharacterAbilities'
      })

      .state('character.inventory', {
        url: '/inventory',
        templateUrl: 'html/partials/character.inventory.html',
        controller: 'CharacterInventory'
      })
	}
);