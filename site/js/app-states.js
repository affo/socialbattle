angular.module('states', ['ui.router'])

.config(

	function($stateProvider){
		$stateProvider

    .state('home', {
      url: '/',
      templateUrl: 'html/partials/home.html',
      controller: 'Auth',
    })

    .state('user', {
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
        templateUrl: 'html/partials/user.posts.html',
        controller: 'UserPosts'
      })

        .state('user.posts.comments', {
          url: '/:post_id/comments',
          templateUrl: 'html/partials/comments.html',
          controller: 'PostComments'
        })

      .state('user.characters', {
        url: '/characters',
        templateUrl: 'html/partials/user.characters.html',
        controller: 'UserCharacters'
      })
	}
);