angular.module('states', [])

.config(
  ['$stateProvider',
	function($stateProvider){
		$stateProvider

    .state('unlogged', {
      url: '/',
      templateUrl: 'html/home.html',
      controller: 'Auth',
    })

    .state('logged', {
      templateUrl: 'html/layout.html',
      controller: 'Logged',

      onEnter: ['LoginService',
      function(LoginService){
        LoginService.check_login();
      }],

      resolve: {
        user: ['$localStorage', 'Restangular',
        function($localStorage, Restangular){
          return Restangular.one('me').get()
          .then(
            function(response){
              var user = Restangular.stripRestangular(response);
              return user;
            },
            function(response){
              console.log(response);
              return undefined;
            }
          );
        }], 
      },
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

      url: '/rooms/pve/:room_name',
      templateUrl: 'html/partials/pveroom.html',

      resolve: {
        character: ['$localStorage', 'Restangular', '$modal',
        function($localStorage, Restangular, $modal){
          return Restangular.one('characters', $localStorage.character).get()
          .then(
            function(response){
              var character = Restangular.stripRestangular(response);
              return character;
            },
            function(response){
              console.log(response);
            }
          );
        }],

        character_abilities: ['$localStorage', 'Restangular', 
        function($localStorage, Restangular){
          return Restangular.one('characters', $localStorage.character).getList('abilities')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(response);
              return obj;
            }
          );
        }],

        weapons: ['$localStorage', 'Restangular',
        function($localStorage, Restangular){
          return Restangular.one('characters', $localStorage.character).getList('weapons')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(response);
              return obj;
            }
          );
        }],

        armors: ['$localStorage', 'Restangular',
        function($localStorage, Restangular){
          return Restangular.one('characters', $localStorage.character).getList('armors')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(response);
              return obj;
            }
          );
        }],

        items: ['$localStorage', 'Restangular',
        function($localStorage, Restangular){
          return Restangular.one('characters', $localStorage.character).getList('items')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(response);
              return obj;
            }
          );
        }],

        mobs: ['$stateParams', 'Restangular',
        function($stateParams, Restangular){
          return Restangular.one('rooms/pve', $stateParams.room_name).getList('mobs')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(response);
              return obj;
            }
          );
        }],

        room: ['$stateParams', 'Restangular',
        function($stateParams, Restangular){
          return Restangular.one('rooms/pve', $stateParams.room_name).get()
          .then(
            function(response){
              var obj = Restangular.stripRestangular(response);
              return obj;
            }
          );
        }],
      },

      controller: 'PVERoom',
    }
    )

    .state('relaxroom', {
      parent: 'logged',

      url: '/rooms/relax/:room_name',
      templateUrl: 'html/partials/relaxroom.html',
      controller: 'RelaxRoom',

     resolve: {
      character: ['$localStorage', 'Restangular', '$modal',
      function($localStorage, Restangular, $modal){
        return Restangular.one('characters', $localStorage.character).get()
        .then(
          function(response){
            var character = Restangular.stripRestangular(response);
            return character;
          },
          function(response){
            console.log(response);
          }
        );
      }],

      room: ['$stateParams', 'Restangular',
      function($stateParams, Restangular){
          return Restangular.one('rooms/relax', $stateParams.room_name).get()
          .then(
            function(response){
              var obj = Restangular.stripRestangular(response);
              return obj;
            }
          );
        }],
      },
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
      });
	}
  ]
);