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
              id: n.id,
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
                id: n.id,
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
          n_endpoint = Restangular.one('notifications', n.id);
          n_endpoint.read = true;
          n_endpoint.put();
        }
      }
    };

  }
  ]
)

.controller('Activities',
  ['$scope', 'Pusher',
  function($scope, Pusher){
    $scope.activities = [];
    var MAX_ACTIVITIES = 7;

    var push_activity = function(activity, type){
      var verb;
      if(activity.op == 'B'){
        verb = 'bought';
      }else if(activity.op == 'S'){
        verb = 'sold';
      }

      $scope.activities.unshift({
        type: type,
        data: activity,
        verb: verb,
      });

      if($scope.activities.length > MAX_ACTIVITIES){
        $scope.activities.pop();
      }
    };

    Pusher.subscribe($scope.username, 'activity-endbattle',
      function(activity){
        push_activity(activity, 'activity-endbattle');
      }
    );
    Pusher.subscribe($scope.username, 'activity-transaction',
      function(activity){
        push_activity(activity, 'activity-transaction');
      }
    );
  }
  ]
);