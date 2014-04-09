'use strict';

/* Controllers */

var ctrls = angular.module('wordsControllers', ['restangular']);

ctrls.controller('WordList',
  function($scope, Restangular) {
    console.log("List controller called");
    $scope.words = Restangular.all('api/words').getList().$object;
  });

ctrls.controller('WordDetail',
  function($scope, $stateParams, Restangular) {
    console.log("Detail controller called");
    $scope.word = Restangular.one('api/words', $stateParams.word_id).get().$object;
  });
