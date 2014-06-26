'use strict';

/**
 * @ngdoc function
 * @name consumerApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the consumerApp
 */
angular.module('consumerApp')
  .controller('MainCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  })


  .controller('SocialBattle',
  	['$scope', '$http', '$location',
  	function($scope, $http, $location){
  		var BASE_URL = 'https://socialbattle-api.herokuapp.com/';
  		var APP_ID = 'cPLF6-E6Hew_DcU8@!GP;M;=_jspTe5sHJoiUcNh';
  		$scope.uri = BASE_URL + 'oauth/authorize/?client_id=' + encodeURIComponent(APP_ID) + '&response_type=token';

  		

  		var states = {
  			no_token: {
  				id: 0,
  				next: function(){
  					$scope.error_msg = 'Oh snap! Something went wrong...';

  					//get the access token,
			  		var params = $location.path().substr(1).split('&');
			  		var token;
			  		for(var i = 0; i < params.length; i++){
			  			var key = params[i].split('=')[0];
			  			var value = params[i].split('=')[1];
			  			if(key === 'access_token'){
			  				token = value;
			  				//hide information
			  				//$location.path() = '/';
			  				break;
			  			}
			  		}
			  		console.log(token);

			  		if(token){
						//set headers
						$http.defaults.headers.common.Authorization = 'Bearer ' + token;
						$http.get(BASE_URL + 'me/')
						.success(
							function(user){
								$http.get(user.url + 'characters/')
								.success(
									function(characters){
										$scope.characters = characters;
										$scope.current_state = states.characters;
									}
								)
								.error(
			  						function(){
			  							$scope.current_state = states.error;
			  						}
			  					);
							}
						)
						.error(
	  						function(){
	  							$scope.current_state = states.error;
	  						}
	  					);
			  		}
  				}
  			},

  			characters: {
  				id: 1,
  				next: function(character){
  					var data = {character: character.url};
  					$http.post(BASE_URL + 'gifts/', data)
  					.success(
  						function(gift){
  							$scope.character_name = character.name;
  							$scope.item_name = gift.name;
  							$scope.current_state = states.gift_given;
  						}
  					)
  					.error(
  						function(){
  							$scope.error_msg = 'Too many gifts for you today';
  							$scope.current_state = states.error;
  						}
  					);
  				}
  			},

  			gift_given: {
  				id: 2,
  				next: function(){
  					$scope.current_state = states.no_token;
  				}
  			},

  			error: {
  				id: 'error',
  				next: function(){
  					$scope.current_state = states.no_token;
  				}
  			}
  		};

  		$scope.current_state = states.no_token;
  		$scope.current_state.next();
  	}
  	]
  );
