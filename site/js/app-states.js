angular.module('states', [])

.config(
  ['$stateProvider',
	function($stateProvider){
		$stateProvider

    .state('unlogged', {
      url: '/',
      templateUrl: 'html/home.html',
      controller: 'Auth',

      onEnter: ['IdentityService', '$state',
        function(IdentityService, $state){
          IdentityService.identity()
          .then(
            function(identity){
              $state.go('user', {username: identity.username});
            }
          );
        }
      ],
      
    })

    .state('logged', {
      templateUrl: 'html/layout.html',
      abstract: true,
      controller: 'Logged',
      resolve: {
        authorize: ['CheckAuthService',
          function(CheckAuthService) {
            return CheckAuthService.check_auth();
          }
        ],

        user: ['IdentityService', 
          function(IdentityService){
            return IdentityService.identity()
            .then(
              function(identity){
                return identity;
              }
            );
          }
        ]
      }
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

      .state('user.notifications', {
        url: '/notifications',
        templateUrl: 'html/partials/user.notifications.html',
        controller: 'UserNotifications'
      })

      .state('user.posts', {
        url: '/posts',
        templateUrl: 'html/partials/posts.html',
        controller: 'UserPosts',

        resolve: {
          character: ['$localStorage', 'Restangular',
          function($localStorage, Restangular){
            return Restangular.one('characters', $localStorage.character.name).get()
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

          inventory: ['$localStorage', 'Restangular',
          function($localStorage, Restangular){
            return Restangular.one('characters', $localStorage.character.name)
            .getList('inventory')
            .then(
              function(response){
                var inventory = Restangular.stripRestangular(response);
                return inventory;
              },
              function(response){
                console.log(response);
              }
            );
          }],
        }
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
          return Restangular.one('characters', $localStorage.character.name).get()
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
          return Restangular.one('characters', $localStorage.character.name).getList('abilities')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(response);
              return obj;
            }
          );
        }],

        weapons: ['$localStorage', 'Restangular',
        function($localStorage, Restangular){
          return Restangular.one('characters', $localStorage.character.name).getList('weapons')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(response);
              return obj;
            }
          );
        }],

        armors: ['$localStorage', 'Restangular',
        function($localStorage, Restangular){
          return Restangular.one('characters', $localStorage.character.name).getList('armors')
          .then(
            function(response){
              var obj = Restangular.stripRestangular(response);
              return obj;
            }
          );
        }],

        items: ['$localStorage', 'Restangular',
        function($localStorage, Restangular){
          return Restangular.one('characters', $localStorage.character.name).getList('items')
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
      character: ['$localStorage', 'Restangular',
      function($localStorage, Restangular){
        return Restangular.one('characters', $localStorage.character.name).get()
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

      inventory: ['$localStorage', 'Restangular',
      function($localStorage, Restangular){
          return Restangular.one('characters', $localStorage.character.name)
          .getList('inventory')
          .then(
            function(response){
              var inventory = Restangular.stripRestangular(response);
              return inventory;
            },
            function(response){
              console.log(response);
            }
          );
        }],

      buy_items: ['$stateParams', 'Restangular',
      function($stateParams, Restangular){
          return Restangular.one('rooms/relax', $stateParams.room_name)
          .getList('items')
          .then(
            function(response){
              var buy_items = Restangular.stripRestangular(response);
              return buy_items;
            },
            function(response){
              console.log(response);
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
      })

  .state('post', {
    parent: 'logged',

    url: '/posts/:id/',
    resolve: {
      character: ['$localStorage', 'Restangular',
      function($localStorage, Restangular){
        return Restangular.one('characters', $localStorage.character.name).get()
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

      inventory: ['$localStorage', 'Restangular',
      function($localStorage, Restangular){
        return Restangular.one('characters', $localStorage.character.name)
        .getList('inventory')
        .then(
          function(response){
            var inventory = Restangular.stripRestangular(response);
            return inventory;
          },
          function(response){
            console.log(response);
          }
        );
      }],

      post: ['$stateParams', 'Restangular',
      function($stateParams, Restangular){
        return Restangular.one('posts', $stateParams.id)
        .get()
        .then(
          function(response){
            var post = Restangular.stripRestangular(response);
            return post;
          },
          function(response){
            console.log(response);
          }
        );
      }]
    },

    controller: [
      '$scope', 'character', 'inventory', 'post',
      function($scope, character, inventory, post){
        $scope.character = character;
        $scope.inventory = inventory;
        $scope.post = post;
      }
    ],
    template: '<post post="post" ng-controller="Post"/>'
  });

	}
  ]
);