angular.module('search', ['restangular'])

.controller('Search', function($scope, Restangular, $localStorage){
	var users = Restangular.all('users');
	var rooms = Restangular.all('rooms');
	$scope.searchForm = {};
	$scope.results = {};
	$scope.searching = false;

	//some view logic for the search bar
	// angular.element('#searchbar').on('blur', function(e){
	// 	$scope.$apply(function(){$scope.searching = false;});
	// });

	angular.element('#searchbar').on('focusin', function(e){
		$scope.$apply(function(){
			if($scope.searchForm.query){
				$scope.searching = true;
			}
		});
	});
	
	var keys = {
		LEFT: 37,
		UP: 38,
		RIGHT: 39,
		DOWN: 40,
		ENTER: 13,
		ESC: 27,
	}

	$scope.keypressed = function($event){
		//console.log($event.which);
		var key = $event.which;
		if(key == keys.LEFT || key == keys.RIGHT){
			//does nothing
		}else if(key == keys.UP){

		}else if(key == keys.DOWN){

		}else if(key == keys.ESC){
			$scope.submit();
		}else{
			$scope.search();
		}
	};

	$scope.submit = function(){
		$scope.searching = false;
		$scope.searchForm = {};
		$scope.results = {};
	};

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