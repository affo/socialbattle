angular.module('directives', [])

.directive('post',
  function(){
    return {
      templateUrl: 'html/templates/post.html',
      scope: true,
    };
  }
)

.directive('twitter',
  function(){
    return {
      template: "<h1>CIAO BOMBER</h1>",
      scope: true,
    };
  }
)

.directive('notification',
  function(){
    return {
      templateUrl: 'html/templates/notification.html',
      scope: true,
    };
  }
)