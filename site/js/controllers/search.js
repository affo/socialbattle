angular.module('search', [])

.controller('Search',
  ['$scope', 'Restangular', '$localStorage', '$state',
  function($scope, Restangular, $localStorage, $state){
    var users_endpoint = Restangular.all('users');
    var rooms_endpoint = Restangular.all('rooms');
    $scope.searchForm = {};
    $scope.results = [];
    
    var keys = {
      LEFT: 37,
      UP: 38,
      RIGHT: 39,
      DOWN: 40,
      ENTER: 13,
      ESC: 27,
    };

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

      users_endpoint.customGET('', {query: query})
      .then(
        function(response){
          var users = Restangular.stripRestangular(response);
          $scope.results = users;
        }
      );
    };
  }
  ]
);