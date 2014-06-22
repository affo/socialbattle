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
        $scope.notifications.push({
          type: 'fellow',
          data: notification,
        });
      }
    );
    Pusher.subscribe(user.username, 'comment',
      function(notification){
        $scope.notifications.push({
          type: 'comment',
          data: notification,
        });
      }
    );
    Pusher.subscribe(user.username, 'accept',
      function(notification){
        $scope.notifications.push({
          type: 'accept',
          data: notification,
        });
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

    //get notifications
    Restangular.one('users', $localStorage.user.username)
    .one('notifications/unread').get()
    .then(
      function(response){
        var notifications = Restangular.stripRestangular(response);
        $scope.notifications = notifications.results.map(
          function(n){
            return {
              type: n.activity.event,
              data: n.activity.data
            };
          }
        );
        $scope.no_unread = notifications.count;
      }
    );

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