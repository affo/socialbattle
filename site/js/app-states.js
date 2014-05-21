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

    .state('user-detail.following', {
      url: '/following',
      templateUrl: 'html/partials/user-detail.followx.html',
      controller: 'UserFollowing'
    })

    .state('user-detail.followers', {
      url: '/followers',
      templateUrl: 'html/partials/user-detail.followx.html',
      controller: 'UserFollowers'
    })

    .state('user-detail.posts', {
      url: '/posts',
      templateUrl: 'html/partials/user-detail.posts.html',
      controller: 'UserPosts'
    })

    .state('user-detail.characters', {
      url: '/characters',
      templateUrl: 'html/partials/user-detail.characters.html',
      controller: 'UserCharacters'
    })
	}
);