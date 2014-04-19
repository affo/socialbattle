'use strict';

/* Controllers */

var ctrls = angular.module('wordsControllers', ['restangular']);

ctrls.controller('UserList',
  function($scope, Restangular) {
    console.log("List controller called");
    $scope.users = Restangular.all('api/users').getList().$object;

    // $scope.submit = function(){
    // 	//post
    // 	var word = {word: $scope.text};
    //     //var enc = base64.encode('root:rot');
    //     //Restangular.setDefaultHeaders({'Authorization': 'Basic root:root'});
    // 	Restangular.all('api/words/').
    //             post(word).then(function(){
    // 		console.log('New word saved');
    // 		$scope.words = Restangular.all('api/words').getList().$object;
    // 	},
    // 	function(){
    // 		console.log('Error on saving');
    // 	});
    // 	$scope.text = '';
    // }
  });

ctrls.controller('UserDetail',
  function($scope, $stateParams, Restangular) {
    console.log("Detail controller called");
    $scope.user = Restangular.one('api/users', $stateParams.user_id).get().$object;
  });
