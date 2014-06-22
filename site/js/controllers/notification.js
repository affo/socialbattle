angular.module('notification', [])

.controller('UserNotifications',
	['$scope', '$localStorage', 'Restangular',
	function($scope, $localStorage, Restangular){
		Restangular.one('users', $localStorage.user.username)
    .one('notifications').get()
    .then(
      function(response){
        var notifications = Restangular.stripRestangular(response);
        $scope.next = notifications.next;
        $scope.notifications = notifications.results.map(
          function(n){
            return {
              type: n.activity.event,
              data: n.activity.data
            };
          }
        );
      }
    );

    $scope.next_page = function(){
	    Restangular.oneUrl('next_page', $scope.next).get().
	    then(
	      function(response){
	        for(var i = 0; i < response.results.length; i++){
	          $scope.notifications.push(
	          	{
	              type: response.results[i].activity.event,
	              data: response.results[i].activity.data
	            }
	          );
	        }

	        if(response.next){
	          $scope.next = response.next;
	        }else{
	          $scope.next = undefined;
	        }
	      }
	    );
	  };

	}
	]
);