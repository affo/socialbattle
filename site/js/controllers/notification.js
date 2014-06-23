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
              data: n.activity.data,
              url: n.url,
              read: n.read,
            };
          }
        );

        //sign as read the first notifications
        $scope.read();
      }
    );

    $scope.next_page = function(){
      Restangular.oneUrl('next_page', $scope.next).get().
      then(
        function(response){
          var n;
          for(var i = 0; i < response.results.length; i++){
            n = response.results[i];
            $scope.notifications.push(
              {
                type: n.activity.event,
                data: n.activity.data,
                url: n.url,
                read: n.read,
              }
            );
          }

          if(response.next){
            $scope.next = response.next;
          }else{
            $scope.next = undefined;
          }

          $scope.read();
        }
      );
    };

    $scope.read = function(){
      var n_endpoint;
      var n;
      for(var i = 0; i < $scope.notifications.length; i++){
        n = $scope.notifications[i];
        if(!n.read){
          n_endpoint = Restangular.oneUrl('notification', n.url);
          n_endpoint.read = true;
          n_endpoint.put();
        }
      }
    };

  }
  ]
);