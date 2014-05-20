angular.module('states', ['ui.router'])

.config(

	function($stateProvider){
		$stateProvider

    .state('home', {
      url: '/',
      templateUrl: 'html/partials/home.html',
      controller: 'Auth',
    })

    .state('user-detail', {
      url: '/users/:username',
      templateUrl: 'html/partials/user-detail.html',
      controller: 'UserDetail'
    })

    .state('user-detail.follows', {
      url: '/follows',
      templateUrl: 'html/partials/user-detail.follows.html',
      controller: 'UserFollows'
    })
	}
);