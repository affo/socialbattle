angular.module('main', ['restangular', 'ngStorage', 'facebook'])

.controller('Main',
  function($scope, $state, $localStorage, Restangular){
    // var t = new Trianglify({cellsize: 200});
    // var pattern = t.generate(200, 200);
    // $scope.triang = pattern.dataUrl;

    if($localStorage.logged){
      $scope.$storage = $localStorage;
      Restangular.setDefaultHeaders({'Authorization': 'Token ' + $localStorage.token});
    }else{
      //no user logged... redirected to home page
      $state.go('home');
    }
})