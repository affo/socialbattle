var app = angular.module('socialBattle', [
  'ui.router', 'states',
  'restangular',
  'facebook',
  'ngStorage',
  'ui.bootstrap',
  
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

app.constant('CLIENT_ID', '.N?CHW4tRAgfvLNrq3ThSlVL9DsRxqDnA@5Grl2R');