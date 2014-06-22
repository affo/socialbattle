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
  'notification',
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
    //@ifndef HEROKU
    RestangularProvider.setBaseUrl('http://localhost.socialbattle:8000/');
    //@endif

    //@ifdef HEROKU
    RestangularProvider.setBaseUrl('https://socialbattle-api.herokuapp.com/');
    //@endif

    RestangularProvider.setRequestSuffix('/');
  }
  ]
);

app.config(['FacebookProvider', function(FacebookProvider) {
    // Here you could set your appId through the setAppId method and then initialize
    // or use the shortcut in the initialize method directly.

    //@ifdef HEROKU
    FacebookProvider.init('1441968896050367');
    //@endif

    //@ifndef HEROKU
    FacebookProvider.init('1451410555106201');
    //@endif
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
//@ifdef HEROKU
app.constant('API_URL', 'https://socialbattle-api.herokuapp.com/');
//@endif

//@ifndef HEROKU
app.constant('API_URL', 'http://localhost.socialbattle:8000/');
//@endif
