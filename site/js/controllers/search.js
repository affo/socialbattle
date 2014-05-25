angular.module('search', ['restangular'])

.controller('Search', function($scope, Restangular, $localStorage){
	var users = Restangular.all('users');
	var rooms = Restangular.all('rooms');
	$scope.searchForm = {};
	$scope.results = {};
	$scope.searching = false;

	//some view logic for the search bar
	angular.element('#searchbar').on('focusout', function(e){
		$scope.$apply(function(){$scope.searching = false;});	
	});

	angular.element('#searchbar').on('focusin', function(e){
		$scope.$apply(function(){
			if($scope.searchForm.query){
				$scope.searching = true;	
			}
		});
	});

	$scope.search = function(){
		var query = $scope.searchForm.query;
		if(!query){
			$scope.searching = false;
			return;
		}

		$scope.searching = true;

		//start with users
		users.customGET('', {query: query})
		.then(
			function(users){
				$scope.results.users = users;
			}
		);

		//eventually, rooms
		rooms.customGET('', {query: query})
		.then(
			function(rooms){
				$scope.results.rooms = rooms;
			}
		);
	}

});