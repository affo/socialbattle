var app = angular.module('socialBattle', [
  'ui.router', 'states',
  'restangular',
  'facebook',
  'ngStorage',
  'ui.bootstrap',
  
  'services',
  'auth',
  'user',
  'room',
  'post',
  'search',
  'settings',
  'logged',
  'character',
]);

app.run(
    ['$rootScope', '$state', '$stateParams',
    function($rootScope, $state, $stateParams) {

      // It's very handy to add references to $state and $stateParams to the $rootScope
      // so that you can access them from any scope within your applications.For example,
      // <li ui-sref-active="active }"> will set the <li> // to active whenever
      // 'contacts.list' or one of its decendents is active.
      $rootScope.$state = $state;
      $rootScope.$stateParams = $stateParams;
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

app.constant('CLIENT_ID', 'muswW5o!U_hOlfOaK_ai7pMMHX7-1vggQY5yPGGA');