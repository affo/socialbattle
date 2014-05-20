angular.module('main', ['restangular', 'ngStorage', 'facebook'])

.controller('Main',
	function($scope, $state, $localStorage, Restangular){
		if($localStorage.logged){
			$scope.$storage = $localStorage;
			Restangular.setDefaultHeaders({'Authorization': 'Token ' + $localStorage.token});

			$scope.logout = function(){ 
	      Restangular.setDefaultHeaders(
	          {'Authorization': ''}
	      );
	      delete $localStorage.token;
	      delete $localStorage.logged;
	      delete $localStorage.user;
				$state.go('home');	      
    	};
		}else{
			//no user logged... redirected to home page
			$state.go('home');
		}
})