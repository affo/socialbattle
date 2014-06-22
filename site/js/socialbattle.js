var app = angular.module('socialBattle', [
  'angular-loading-bar',
  'ui.router', 'states',
  'restangular',
  'facebook',
  'ngStorage',
  'ui.bootstrap',
  'doowb.angular-pusher',
  
  'services',
  'directives',
  'auth',
  'user',
  'room',
  'post',
  'search',
  'character',
]);

app.run(
  ['$rootScope', '$state', '$stateParams', 'CheckAuthService',
    'IdentityService', 'RefreshTokenService', 'Restangular', '$localStorage',
  function($rootScope, $state, $stateParams, CheckAuthService,
            IdentityService, RefreshTokenService, Restangular, $localStorage){
    
    RefreshTokenService.init();

    $rootScope.$on('$stateChangeStart',
      function(event, toState, toStateParams){
        $rootScope.toState = toState;
        $rootScope.toStateParams = toStateParams;

        CheckAuthService.check_auth();
      }
    );

    Restangular.setDefaultHeaders({Authorization: 'Bearer ' + $localStorage.access_token});

  }
  ]
);

app.config(
  ['RestangularProvider',
  function(RestangularProvider){
    RestangularProvider.setBaseUrl('http://localhost.socialbattle:8000/');
    RestangularProvider.setRequestSuffix('/');
  }
  ]
);

app.config(['FacebookProvider', function(FacebookProvider) {
    // Here you could set your appId through the setAppId method and then initialize
    // or use the shortcut in the initialize method directly.

    FacebookProvider.init('1451410555106201');
}]);

app.config(
  ['$urlRouterProvider',
  function($urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
  }
  ]
);

app.config(['cfpLoadingBarProvider',
  function(cfpLoadingBarProvider) {
    cfpLoadingBarProvider.includeSpinner = false;
  }
  ]
);

app.config(['PusherServiceProvider',
  function(PusherServiceProvider){
    PusherServiceProvider
      .setToken('3863968fa562d8ec8569')
      .setOptions({});
  }
]);

app.constant('CLIENT_ID', 'hHH7dFdb=KpR0gpJVSiEO6rKArllw9e@=w=-?Gl1');
app.constant('API_URL', 'http://localhost.socialbattle:8000/');

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
angular.module('services', ['socialBattle'])

.factory('SpawnService',
  ['$q', '$timeout', 'Restangular',
  function($q, $timeout, Restangular){
    var factory = {};
    var TIMEOUT_RANGE = [5, 10].map(function(x){ return x * 1000;}); //timeout range in ms
    var timeout_promise;
    var deferred;

    //returns a promise containing a mob
    factory.spawn = function(mobs){
      if(mobs.length === 0) return {};
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
  ]
)

.factory('AttackService',
  ['$q', '$timeout', 'Restangular',
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
  ]
)

.factory('MobService',
  ['Restangular', 'AttackService',
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
    };

    return factory;
  }
  ]
)

.factory('CharacterService',
  ['Restangular', 'AttackService',
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
  ]
)

.factory('FBStoriesService',
  ['Facebook', '$localStorage',
  function(Facebook, $localStorage){
    var factory = {};

    factory.APP_NAMESPACE = 'socialbattle_test';
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
  ]
)

.factory('IdentityService',
  ['$q', '$http', '$timeout', 'Restangular', '$localStorage',
  function($q, $http, $timeout, Restangular, $localStorage){
    var _identity = undefined;
    var _authenticated = false;
    var factory = {};

    
    factory.isIdentityResolved = function(){
      return angular.isDefined(_identity);
    };

    factory.isAuthenticated = function(){
      return _authenticated;
    };
      
    factory.authenticate = function(identity){
      _identity = identity;
      _authenticated = angular.isDefined(identity);
      
      if(identity){
        $localStorage.user = identity;
      } else {
        delete $localStorage.user;
      }
    };

    factory.identity = function(force){
      var deferred = $q.defer();

      if (force === true) _identity = undefined;

      // check and see if we have retrieved the identity data from the server. if we have, reuse it by immediately resolving
      if (angular.isDefined(_identity)) {
        deferred.resolve(_identity);

        return deferred.promise;
      }

      Restangular.one('me').get()
      .then(
        function(response){
          var user = Restangular.stripRestangular(response);
          _identity = user;
          _authenticated = true;
          deferred.resolve(_identity);
        },
        function(response){
          _identity = undefined;
          _authenticated = false;
          deferred.reject(_identity);
        }
      );
      

      return deferred.promise;
    };

    return factory;
  }
  ]
)

.factory('CheckAuthService',
  ['$rootScope', '$state', 'IdentityService', 'RefreshTokenService',
  function($rootScope, $state, IdentityService, RefreshTokenService){
    var factory = {};

    factory.check_auth = function(){
      return IdentityService.identity()
      .then(
        function(identity){
          //everything is ok 
          //$state.go('user.posts', {username: identity.username});
        },
        function(error){
          //not auth
          if(!RefreshTokenService.refreshing){
            $state.go('unlogged');
          }
        }
      );
    };

    return factory;
  }
  ]
)

.factory('LoginService',
  ['Facebook', '$localStorage', 'Restangular', '$q', '$state',
    'CLIENT_ID', 'IdentityService',
  function(Facebook, $localStorage, Restangular, $q, $state,
            CLIENT_ID, IdentityService){
    var factory = {};

    var set_header = function(token){
      Restangular.setDefaultHeaders({Authorization: 'Bearer ' + token});
    };

    factory.sb_login = function(username, password){
      var deferred = $q.defer();
      var data = {
            grant_type: "password",
            client_id: CLIENT_ID,
            username: username,
            password: password,
      };

      //encode the request
      data = $.param(data);

      Restangular.all('oauth/token').post(data, undefined, {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      })
      .then(
        function(response){
            console.log(response);
            $localStorage.refresh_token = response.refresh_token;
            $localStorage.access_token = response.access_token;
            set_header(response.access_token);
            IdentityService.identity(true)
            .then(
              function(identity){
                IdentityService.authenticate(identity);
                deferred.resolve(identity);
              },
              function(response){
                //something went wrong
                deferred.reject(response);
              }
            );
        },
        function(response){
            console.log(response);
            deferred.reject(response);
        }
      );
      return deferred.promise;
    };

    factory.fb_login = function(){
      var deferred = $q.defer();

      var get_token_from_fb_token = function(response){
        var data = {
          grant_type: "password",
          client_id: CLIENT_ID,
          username: 'invalid username',
          //invalid username with spaces
          //in this way it won't match anyone
          password: 'password',
          fb_token: response.authResponse.accessToken,
        };

        //encode the request
        data = $.param(data);

        Restangular.all('oauth/token').post(data, undefined, {
          'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        })
        .then(
          function(response){
            $localStorage.facebook = true;
            $localStorage.refresh_token = response.refresh_token;
            $localStorage.access_token = response.access_token;
            set_header(response.access_token);
            IdentityService.identity(true)
            .then(
              function(identity){
                IdentityService.authenticate(identity);
                deferred.resolve(identity);
              },
              function(response){
                //something went wrong
                deferred.reject(response);
              }
            );
          }, function(response){
            deferred.reject(response);
          }
        );
      };

      Facebook.getLoginStatus(
        function(response){
          if(response.status == 'connected') {
              console.log('fb connected');
              get_token_from_fb_token(response);
          }else if(response.status === 'not_authorized'){
            // The person is logged into Facebook, but not your app.
            // and so I'm very sorry...
            deferred.reject(response.status);
          } else {
            // The person is not logged into Facebook, so we're not sure if
            // they are logged into this app or not.
            // let's make him log in to Facebook
            Facebook.login(function(response){
              if(response.authResponse){
                get_token_from_fb_token(response);
              }else{
                //the user stopped the auth
              }
            }, {scope: 'publish_actions'});
          }
        }
      );

      return deferred.promise;
    };

    return factory;
  }
  ]
)

.factory('RefreshTokenService',
  ['$localStorage', 'Restangular', '$q', '$http', 'CLIENT_ID',
  function($localStorage, Restangular, $q, $http, CLIENT_ID){
    var factory = {};
    var _refreshing = false;
    var _deferred;

    var set_header = function(token){
      Restangular.setDefaultHeaders({Authorization: 'Bearer ' + token});
    };

    var refreshAccesstoken = function(){
      if(!$localStorage.refresh_token){
        //there is no refresh_token!
        _deferred = $q.defer();
        _deferred.reject('No refresh token');
        return _deferred.promise;
      }

      if(_refreshing){
        return _deferred.promise; //in case of multiple requests, if someone else is refreshing I wait
      }else{
        _refreshing = true;
      }

      _deferred = $q.defer();

      var data = {
        grant_type: "refresh_token",
        client_id: CLIENT_ID,
        refresh_token: $localStorage.refresh_token,
      };

      console.info('Token expired. Refreshing...');

      //encode the request
      data = $.param(data);

      Restangular.all('oauth/token').post(data, undefined, {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      }).then(
        function(response){
          $localStorage.refresh_token = response.refresh_token;
          $localStorage.access_token = response.access_token;
          set_header(response.access_token);
          _refreshing = false;
          _deferred.resolve('Refreshed');
        },
        function(response){
          console.log(response);
          _deferred.reject('Error');
        }
      );

      return _deferred.promise;
    };

    factory.refreshing = _refreshing;

    factory.init = function(){
      Restangular.setErrorInterceptor(
        function(response, deferred, responseHandler){
          if(response.status === 401) {
              refreshAccesstoken()
              .then(
                function(msg){
                  console.info(msg);
                  // update headers
                  response.config.headers = Restangular.defaultHeaders;
                  // Repeat the request and then call the handlers the usual way.
                  $http(response.config).then(responseHandler, deferred.reject);
                  // Be aware that no request interceptors are called this way.
                }
              );

              return false; // error handled
          }

          return true; // error not handled
        }
      );
    };

    return factory;
  }
  ]
);
angular.module('directives', [])

.directive('post',
  function(){
    return {
      templateUrl: 'html/templates/post.html',
      scope: true,
    };
  }
)

.directive('twitter',
  function(){
    return {
      template: "<h1>CIAO BOMBER</h1>",
      scope: true,
    };
  }
);
angular.module('auth', ['restangular', 'ngStorage', 'facebook'])

.controller('Auth',
  ['$scope', 'Restangular', '$localStorage', 'Facebook',
    '$state', 'LoginService',
  function($scope, Restangular, $localStorage, Facebook,
            $state, LoginService){
    $scope.$storage = $localStorage;
    $scope.alerts = [];
    $scope.signinForm = {};
    $scope.signupForm = {};

    $scope.fb_login = function(){
      LoginService.fb_login()
      .then(
        function(identity){
          $state.go('user', {username: identity.username});
        },
        function(response){
          $scope.alerts.push({type: 'danger', msg: response.data});
        }
      );
    };


    $scope.sb_login = function(){
        LoginService.sb_login($scope.signinForm.username, $scope.signinForm.password)
        .then(
          function(identity){
            $state.go('user', {username: identity.username});
          },
          function(response){
            $scope.alerts.push({type: 'danger', msg: response.data});
          }
        );
    };

    $scope.signup = function(){
        var data = {
            username: $scope.signupForm.username,
            email: $scope.signupForm.email,
            password: $scope.signupForm.password,
        };

        var check = $scope.signupForm.check_password;

        if(check != data.password){
          $scope.alerts.push({type: 'danger', msg: 'The two passwords are different!'});
          $scope.signupForm.password = '';
          $scope.signupForm.check_password = '';
          return;
        }

        Restangular.all('signup').post(data).then(
            function(response){
                $scope.alerts.push({type: 'success', msg: 'Succesfully signed up!'});
                $scope.signupForm = {};
            },
            function(response){
                $scope.alerts.push({type: 'danger', msg: response.data});
            });
    };

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };
  }
  ]
)

.controller('Logged',
  ['$scope', '$stateParams', 'Restangular', '$state',
    '$localStorage', '$modal', 'user', 'IdentityService',
    '$http', 'Facebook', 'API_URL', 'Pusher',
  function($scope, $stateParams, Restangular, $state, $localStorage, $modal, user,
            IdentityService, $http, Facebook, API_URL, Pusher){
    $scope.$storage = $localStorage;
    $scope.username = user.username;
    $scope.facebook = $localStorage.facebook;

    $scope.devcenter_url = API_URL + 'oauth/applications/';

    $scope.notifications = [];
    //subscribe to pusher channel(s)
    Pusher.subscribe(user.username, 'fellow',
      function(notification){
        $scope.notifications.push(notification);
      }
    );

    if(!$localStorage.character){
      var modalInstance = $modal.open({
        templateUrl: 'selectCharacterModal.html',
        controller: 'SelectCharacterModal',
        backdrop: 'static',
        keyboard: false,
        resolve: {
          characters: function(){
            return Restangular.one('users', user.username).getList('characters').$object;
          },

          endpoint: function(){
            return Restangular.one('users', user.username).all('characters');
          }
        }
      });

      modalInstance.result.then(
        function(character){
          $localStorage.character = character;
        }
      );
    }

    $scope.logout = function(){
      IdentityService.authenticate(undefined);
      Restangular.setDefaultHeaders({Authorization: ''});
      delete $localStorage.access_token;
      delete $localStorage.refresh_token;
      delete $localStorage.user;
      delete $localStorage.character;
      delete $localStorage.facebook;
      $state.go('unlogged');
    };

    $scope.ass_facebook = function(){
      console.log('getLoginStatus');
      Facebook.getLoginStatus(function(response){
        $scope.$apply(function(){
          if(response.status == 'connected') {
              console.log('fb connected');
              var data = {access_token: response.authResponse.accessToken};

              Restangular.all('sa/associate/').customGET('facebook', data).then(
                function(user){
                  $localStorage.user = user.username;
                  $localStorage.facebook = true;
                }, function(response){
                  //error
                  console.log(response);
                });
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
                $scope.ass_facebook();
              }else{
                //the user stopped the auth
              }
            }, {scope: 'publish_actions'});
          }
        });
      });
    };

  }
  ]
)

.controller('SelectCharacterModal',
  ['$scope', '$modalInstance', '$localStorage', 'characters', 'endpoint',
    'Restangular',
  function($scope, $modalInstance, $localStorage, characters, endpoint,
            Restangular){
    $scope.characters = characters;
    $scope.characterForm = {};
    $scope.alerts = [];

    $scope.create_character = function(){
      endpoint.post($scope.characterForm)
      .then(
        function(character){
          $scope.select(Restangular.stripRestangular(character));
        },
        function(response){
          $scope.alerts.push({type: 'danger', msg: response.data});
        }
      );
    };

    $scope.select = function(character){
      $modalInstance.close(character);
    };

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };
  }
  ]
);
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
          if(character.name == $localStorage.character.name){
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
angular.module('post', ['restangular'])

.controller('UserPosts',
  ['$scope', 'Restangular', 'character', 'inventory',
  function($scope, Restangular, character, inventory){
    $scope.character = character;
    $scope.inventory = inventory;
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
  ['$scope', 'Restangular', '$localStorage', 'character', 'inventory',
  function($scope, Restangular, $localStorage, character, inventory){
    $scope.postForm = {
      exchanged_items: [],
      character: $localStorage.character.url
    };
    $scope.searched_items = [];
    $scope.alerts = [];
    $scope.can_post = true;
    $scope.character = character;
    $scope.inventory = inventory;

    var _number_given = 1;
    var _number_received = 1;

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };

    $scope.plus_given = function(){
      _number_given++;
      $scope.postForm.exchanged_items.push({given: true});
    };

    $scope.plus_received = function(){
      _number_received++;
      $scope.postForm.exchanged_items.push({given: false});
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
        $scope.search($scope.postForm.exchanged_items[$index].item_name);
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

    $scope.select_given_item = function($item, $model, $label, $index){
      $scope.postForm.exchanged_items[$index].item = $item.item;
    };

    $scope.select_received_item = function($item, $model, $label, $index){
      $scope.postForm.exchanged_items[$index].item = $item;
    };

    $scope.post = function(){
      var post = $scope.postForm;
      if(post.give_guils && isNaN(post.give_guils)){
        $scope.alerts.push({type: "danger", msg: "Given guils must be a number!"});
        return;
      }
      if(post.receive_guils && isNaN(post.receive_guils)){
        $scope.alerts.push({type: "danger", msg: "Received guils must be a number!"});
        return;
      }

      for(var i = 0; i < post.exchanged_items.length; i++){
        var ex = post.exchanged_items[i];
        if(ex.quantity && isNaN(ex.quantity)){
          $scope.alerts.push({type: "danger", msg: "Quantity must be a number!"});
          return;
        }
      }

      post.exchanged_items = post.exchanged_items
      .filter(
        function(ex){
          if(ex.item){
            return true;
          }
          return false;
        }
      );

      post.exchanged_items = post.exchanged_items
      .map(
        function(ex){
          ex.item = ex.item.url;
          if(!ex.quantity) delete ex.quantity;
          return ex;
        }
      );

      $scope.endpoint.all('posts').post(post).then(
        function(post){
          $scope.posts.unshift(post);
          $scope.postForm = {
            exchanged_items: [],
            character: $localStorage.character.url
          };
        },
        function(response){
          $scope.postForm = {
            exchanged_items: [],
            character: $localStorage.character.url
          };
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
  ['$scope', 'Restangular', '$state', '$stateParams',
  function($scope, Restangular, $state, $stateParams){
    var character = $scope.character;
    var inventory = $scope.inventory;
    $scope.comment = {};
    $scope.searched_items = [];
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
      $scope.editPost.exchanged_items.push({given: true});
    };

    $scope.plus_received = function(){
      _number_received++;
      $scope.editPost.exchanged_items.push({given: false});
    };

    var acceptable = function(post){
      if(post.exchanged_items.length === 0){
        $scope.not_acceptable_why = 'No exchange';
        return false;
      }

      if(!post.opened){
        $scope.not_acceptable_why = 'Closed';
        return false;
      }

      if(post.character == character.url){
        $scope.not_acceptable_why = 'Post of yours';
        return false;
      }
      //check guils!
      if(post.receive_guils > character.guils){
        $scope.not_acceptable_why = 'Not enough guils';
        return false;
      }

      exchanges = post.exchanged_items;
      var found = false;
      for(var i = 0; i < exchanges.length; i++){
        var ex = exchanges[i];
        if(!ex.given){
          for(var j = 0; j < inventory.length; j++){
            var record = inventory[j];
            if(record.item.url == ex.item.url && record.quantity < ex.quantity){
              $scope.not_acceptable_why = 'Not enough ' + ex.item.name;
              return false;
            }
            if(record.item.url == ex.item.url && record.quantity >= ex.quantity){
              found = true;
            }
          }

          if(!found){
            $scope.not_acceptable_why = 'Missing item(s)';
            return false;
          }
          found = false;
        }
      }

      return true;
    }

    $scope.acceptable = acceptable($scope.post);

    $scope.toggle_editing = function(){
      //reload post:
      $scope.editPost = Restangular.oneUrl('post', $scope.post.url).get().$object;
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
        $scope.search($scope.editPost.exchanged_items[$index].item.name);
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
      $scope.editPost.exchanged_items[$index].item = $item;
    };

    $scope.select_given_item = function($item, $model, $label, $index){
      $scope.editPost.exchanged_items[$index].item = $item.item;
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
      var post = $scope.editPost;
      if(post.give_guils && isNaN(post.give_guils)){
        $scope.alerts.push({type: "danger", msg: "Given guils must be a number!"});
        return;
      }
      if(post.receive_guils && isNaN(post.receive_guils)){
        $scope.alerts.push({type: "danger", msg: "Received guils must be a number!"});
        return;
      }

      for(var i = 0; i < post.exchanged_items.length; i++){
        var ex = post.exchanged_items[i];
        if(ex.quantity && isNaN(ex.quantity)){
          $scope.alerts.push({type: "danger", msg: "Quantity must be a number!"});
          return;
        }
      }

      post.exchanged_items = post.exchanged_items
      .filter(
        function(ex){
          if(ex.item){
            return true;
          }
          return false;
        }
      );

      post.exchanged_items = post.exchanged_items
      .filter(
        function(ex){
          return ex.item.name.length > 0;
        }
      )
      .map(
        function(ex){
          ex.item = ex.item.url;
          if(!ex.quantity) delete ex.quantity;
          return ex;
        }
      );

      Restangular.oneUrl('post', post.url)
      .customPUT(post).then(
        function(post){
          //update what you are seeing
          $scope.post = Restangular.stripRestangular(post);
          $scope.editPost = $scope.post;
          $scope.toggle_editing();
        },
        function(response){
          console.log(response);
          //reload post:
          $scope.editPost = Restangular.oneUrl('post', $scope.post.url).get().$object;
          $scope.alerts.push({type: "danger", msg: response.data});
        }
      );
    };

    $scope.accept = function(){
      Restangular.oneUrl('post', $scope.post.url)
      .all('accept')
      .post({character: $scope.character.url})
      .then(
        function(response){
          $scope.post = Restangular.stripRestangular(response);
          $scope.acceptable = false;
          //reload state
          $state.transitionTo($state.current, $stateParams, {
              reload: true,
              inherit: false,
              notify: true
          });

          $scope.alerts.push({type: 'success', msg: 'Successfully accepted'});
        },
        function(response){
          $scope.alerts.push({type: 'danger', msg: response.data});
        }
      );

    }

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
                $scope.weapons = Restangular.one('characters', $localStorage.character.name).getList('weapons').$object;
                $scope.armors = Restangular.one('characters', $localStorage.character.name).getList('armors').$object;
                $scope.items = Restangular.one('characters', $localStorage.character.name).getList('items').$object;
                Restangular.one('characters', $localStorage.character.name).get().then(
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
      $state.go('character.inventory', {name: $localStorage.character.name});
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
  ['$scope', 'Restangular', '$state', '$stateParams', '$localStorage', '$modal',
    'Facebook', 'FBStoriesService',
    'character', 'room', 'inventory', 'buy_items',
  function($scope, Restangular, $state, $stateParams, $localStorage, $modal,
            Facebook, FBStoriesService,
            character, room, inventory, buy_items){
    $scope.endpoint = Restangular.one('rooms/relax', $stateParams.room_name);
    $scope.character_endpoint = Restangular.one('characters', $localStorage.character.name);
    $scope.init_msg = 'Welcome, I am the merchant at ' + $stateParams.room_name;
    $scope.sell_items = inventory;
    $scope.buy_items = buy_items;
    $scope.character = character;
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
          for(i = 0; i < buy_items.length; i++){
            if(item_name == buy_items[i].name){
              return buy_items[i];
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
          $state.transitionTo($state.current, $stateParams, {
              reload: true,
              inherit: false,
              notify: true
          });
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
    $scope.user = user.username;
    $scope.action = action.name;
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
angular.module('search', [])

.controller('Search',
  ['$scope', 'Restangular', '$localStorage', '$state',
  function($scope, Restangular, $localStorage, $state){
    var users_endpoint = Restangular.all('users');
    var rooms_endpoint = Restangular.all('rooms');
    $scope.searchForm = {};
    $scope.results = [];
    
    var keys = {
      LEFT: 37,
      UP: 38,
      RIGHT: 39,
      DOWN: 40,
      ENTER: 13,
      ESC: 27,
    };

    $scope.keypressed = function($event){
      //console.log($event.which);
      var key = $event.which;
      if(key == keys.LEFT || key == keys.RIGHT){
        //does nothing
      }else if(key == keys.UP){

      }else if(key == keys.DOWN){

      }else if(key == keys.ESC){
        $scope.submit();
      }else{
        $scope.search();
      }
    };

    $scope.submit = function(){
      $scope.searching = false;
      $scope.searchForm = {};
      $scope.results = {};
    };

    $scope.search = function(){
      var query = $scope.searchForm.query;
      if(!query){
        $scope.searching = false;
        return;
      }

      users_endpoint.customGET('', {query: query})
      .then(
        function(response){
          var users = Restangular.stripRestangular(response);
          $scope.results = users;
        }
      );
    };
  }
  ]
);
angular.module('user', ['restangular'])

.controller('UserDetail',
  ['$scope', '$stateParams', 'Restangular', '$state', '$localStorage', 'user',
  function($scope, $stateParams, Restangular, $state, $localStorage, identity) {
    $scope.identity = identity;
    $scope.endpoint = Restangular.one('users', $stateParams.username);
    $scope.endpoint.get().then(
      function(user){
        $scope.user = user;
        if(user.username == identity.username){
          $scope.isMe = true;
        }

        Restangular.one('users', identity.username)
          .post('isfollowing', {to_user: user.url}).then(
            function(response){
              $scope.alreadyFollowing = response.is_following;
              $scope.fellowship = response.url;
            },
            function(response){
              $scope.alreadyFollowing = false;
            }
        );
      }
    );

    $scope.follow = function(){
      data = {
        to_user: $scope.user.url,
      };
      Restangular.one('users', identity.username).all('following').post(data)
      .then(
        function(response){
          console.log(response);
          $scope.alreadyFollowing = true;
          $scope.fellowship = response.url;
        },
        function(response){
          console.log(response);
        }
      );
    };

    $scope.unfollow = function(){
      Restangular.oneUrl('fellowships', $scope.fellowship).remove().then(
        function(response){
          $scope.alreadyFollowing = false;
        },
        function(response){
          console.log(response);
        }
      );
    };
  }
  ]
)


.controller('UserFollowing',
  ['$scope', 'Restangular',
  function($scope, Restangular) {
    $scope.endpoint.getList('following')
    .then(
      function(response){
        var following = Restangular.stripRestangular(response);
        following = following.map(function(fellowship){
          return fellowship.to_user;
        });
        $scope.followx = following;
      }
    );
  }
  ]
)

.controller('UserFollowers',
  ['$scope', 'Restangular',
  function($scope, Restangular) {
    $scope.endpoint.getList('followers')
    .then(
      function(response){
        var followers = Restangular.stripRestangular(response);
        followers = followers.map(function(fellowship){
          return fellowship.from_user;
        });
        $scope.followx = followers;
      }
    );
  }
  ]
)

.controller('UserCharacters',
  ['$scope', 'Restangular', '$localStorage',
  function($scope, Restangular, $localStorage){
    var characters = $scope.endpoint.getList('characters').$object;
    $scope.selected_character = $localStorage.character;
    $scope.characters = characters;
    $scope.characterForm = {};
    $scope.alerts = [];

    $scope.select = function(character){
      $localStorage.character = character;
      $scope.selected_character = character;
    };

    $scope.is_selected = function(character){
      return character.name == $scope.selected_character.name;
    }

    $scope.create_character = function(){
      $scope.endpoint.all('characters').post($scope.characterForm)
      .then(
        function(character){
          $scope.characters.push(character);
          $scope.alerts.push({type: 'success', msg: character.name + ' succesfully created!'});
          $scope.characterForm = {};
        },
        function(response){
          $scope.alerts.push({type: 'danger', msg: response.data});
        }
      );
    };

    $scope.closeAlert = function(index){
      $scope.alerts.splice(index, 1);
    };
  }
  ]
);