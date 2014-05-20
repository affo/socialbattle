angular.module('states', ['ui.router'])

.config(
	function($stateProvider){
		$stateProvider

		.state('unlogged', {
			url: '/',
			templateUrl: 'html/partials/home.html',
			controller: 'Auth',
		})

		.state('logged', {
			resolve: {
				user: function(Restangular, $stateParams, $localStorage){
					Restangular.setDefaultHeaders({'Authorization': 'Token ' + $localStorage.token});
					var username = $stateParams.username;
					return Restangular.all('users').get(username).$object;
				}
			}

			controller: function($scope, user){
				$scope.user = user;
			}
		})

	}
)