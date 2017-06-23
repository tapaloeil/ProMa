var taskControllers=angular.module('taskControllers',[]);

taskControllers.controller('TaskDetailController',['$scope','$routeParams','$http',
	function($scope, $routeParams, $http){
		$http.get('http://localhost:8090/scheduling/api/task/' + $routeParams.taskId + '/?format=json').success(function(data){
			$scope.task=data;
		})
	}

	]);