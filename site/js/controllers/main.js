angular.module('main', ['restangular', 'ngStorage', 'facebook'])

.controller('Main',
  function($scope, $state, $localStorage, Restangular, Facebook){
    // var t = new Trianglify({cellsize: 200});
    // var pattern = t.generate(200, 200);
    // $scope.triang = pattern.dataUrl;
    $scope.logged = false;

    if($localStorage.logged){
      $scope.$storage = $localStorage;
      $scope.logged = true;
      Restangular.setDefaultHeaders({'Authorization': 'Token ' + $localStorage.token});
    }else{
      //no user logged... redirected to home page
      $scope.logged = false;
      $state.go('unlogged');
    }

  }
);