angular.module('room', ['restangular'])

.controller('Rooms',
	function($scope, $state, $localStorage, Restangular){
		$scope.pverooms = Restangular.all('rooms/pve').getList().$object;
		$scope.relaxrooms = Restangular.all('rooms/relax').getList().$object;
})