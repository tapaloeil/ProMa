var taskApp = angular.module('taskApp',['ngRoute', 'taskControllers']);

taskApp.config(['$routeProvider', 
	function ($routeProvider){
		$routeProvider.
			when('/task/:taskId',{
				templateUrl : 'http://localhost:8090/static/html/task-detail.html',
				controller:'TaskDetailController'
			})
	}
]);

taskApp.config(['$httpProvider', 
	function($httpProvider){
		$httpProvider.defaults.xsrfCookieName = 'csrftoken';
		$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	}
]);