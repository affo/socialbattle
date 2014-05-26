angular.module('room', ['restangular'])

.controller('Rooms',
	function($scope, $state, $localStorage, Restangular){
		$scope.pverooms = Restangular.all('rooms/pve').getList().$object;
		$scope.relaxrooms = Restangular.all('rooms/relax').getList().$object;
})

.controller('PVERoom', function($scope, Restangular, $stateParams){
	$scope.endpoint = Restangular.one('rooms/relax', $stateParams.room_name);
	$scope.room_name = $stateParams.room_name;
})

.controller('RelaxRoom', function($scope, Restangular, $stateParams){
	$scope.endpoint = Restangular.one('rooms/relax', $stateParams.room_name);
	$scope.init_msg = 'Welcome, I am the merchant at ' + $stateParams.room_name;
	$scope.items = $scope.endpoint.all('items').getList().$object;
	$scope.msgForm = {};
	$scope.action = 'BUY';
	var init_msg = {
		content: 'Welcome, I am the merchant at ' + $scope.room_name,
		from_merchant: true
	};
	$scope.messages = [];

	$scope.toggle_action = function(){
		if($scope.action == 'BUY'){
			$scope.action = 'SELL';
		}else{
			$scope.action = 'BUY';
		}
	}

	$scope.send = function(){
		var item_name = $scope.msgForm.content
		var sent = {
			content: item_name,
			from_user: true,
		};
		$scope.messages.push(sent);

		//find the item by name
		var index = -1;
		for(var i = 0; i < $scope.items.length; i++){
			if(item_name == $scope.items[i].name){
				index = i;
				break;
			}
		}

		if(index > -1){
			$scope.selected_item = $scope.items[index];
			var msg = {
				content: 'So you want ' + item_name + '... How many?',
				from_merchant: true,
			};
			$scope.messages.push(msg);
		}else{
			var msg = {
				content: 'I do not sell ' + item_name + ', sorry...',
				from_merchant: true,
			};
			$scope.messages.push(msg);
		}
		$scope.msgForm = {};
	}

	$scope.put_item = function(name){
		$scope.msgForm.content = name;
	};

})

.controller('RelaxRoomPosts', function($scope, Restangular){
	$scope.postForm = {};
	$scope.can_post = true;

	$scope.post = function(){
		$scope.endpoint.all('posts').post($scope.postForm).then(
			function(post){
				$scope.posts.unshift(post);
			}
		);
	};

  //because of pagination
  $scope.endpoint.one('posts').get().then(
    function(response){
      $scope.posts = response.results;
      $scope.next = response.next;
    }
  );

  $scope.next_page = function(){
    Restangular.oneUrl('next_page', $scope.next).get().
    then(
      function(response){
        for(var i = 0; i < response.results.length; i++){
          $scope.posts.push(response.results[i]);
        }

        if(response.next){
          $scope.next = response.next;
        }else{
          $scope.next = undefined;
        }
      }
    );

  };
})