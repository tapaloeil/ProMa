'use strict';

/**
 * @ngdoc overview
 * @name angularGanttDemoApp
 * @description
 * # angularGanttDemoApp
 *
 * Main module of the application.
 */

var holidays = [
    {from: new Date(2017,6,14,8,0,0), to: new Date(2017,6,14,20,0,0), name: '14 juillet'},
    {from: new Date(2017,7,15,8,0,0), to: new Date(2017,7,15,20,0,0), name: '15 aout'},
    {from: new Date(2017,10,1,8,0,0), to: new Date(2017,10,1,20,0,0), name: '1 novembre'},
    {from: new Date(2017,10,11,8,0,0), to: new Date(2017,10,11,20,0,0), name: '11 novembre'},
    {from: new Date(2017,11,25,8,0,0), to: new Date(2017,11,25,20,0,0), name: 'noel'},
    {from: new Date(2018,0,1,8,0,0), to: new Date(2018,0,1,20,0,0), name: 'nouvel an'},
    {from: new Date(2017,7,21), to: new Date(2017,8,11), name:"vacances Noémie", classes:["vacances1"]},
    {from: new Date(2017,9,15), to: new Date(2017,10,4), name:"vacances Sylvain", classes:["vacances2"]}
];

var myapp = angular.module('angularGanttDemoApp', [
    'gantt', // angular-gantt.
    'gantt.sortable',
    'gantt.movable',
    'gantt.drawtask',
    'gantt.tooltips',
    'gantt.bounds',
    'gantt.progress',
    'gantt.table',
    'gantt.tree',
    'gantt.corner',
    'gantt.groups',
    'gantt.sections',
    'gantt.dependencies',
    'gantt.overlap',
    'gantt.resizeSensor',
    'ngAnimate',
    'mgcrea.ngStrap'
]).config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{+');
    $interpolateProvider.endSymbol('+}');
}]
);


'use strict';

/**
 * @ngdoc function
 * @name angularGanttDemoApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the angularGanttDemoApp
 */
angular.module('angularGanttDemoApp')
    .controller('MainCtrl', ['$scope', '$http', '$timeout', '$log', 'ganttUtils', 'GanttObjectModel', 'ganttMouseOffset', 'ganttDebounce', 'moment', function($scope,$http, $timeout, $log, utils, ObjectModel, mouseOffset, debounce, moment) {
        var objectModel;
        var dataToRemove;
        
        // Event handler
        var logScrollEvent = function(left, date, direction) {
            if (date !== undefined) {
                $log.info('[Event] api.on.scroll: ' + left + ', ' + (date === undefined ? 'undefined' : date.format()) + ', ' + direction);
            }
        };

        // Event handler
        var logDataEvent = function(eventName) {
            $log.info('[Event] ' + eventName);
        };

        // Event handler
        var logTaskEvent = function(eventName, task) {
            $log.info('[Task Event] ' + eventName + ': ' + task.model.name);
        };

        var ganttapi_dependancy = function(eventName, task){
            var csrftoken = getCookie('csrftoken');
            $.ajaxSetup({
              beforeSend: function(xhr, settings) {
                  if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                      xhr.setRequestHeader("X-CSRFToken", csrftoken);
                  }
              }
            });
            $.ajax({
                url: '/fr/scheduling/api/gantt/dep/'+ task.model.to + '/',
                type: 'GET',
                async:false,
                success: function(data){
                    var pushData=data
                    var deptab=[];
                    deptab=pushData.Dependance;
                    console.log(deptab);
                    //pushData.Dependance.push(task.task.model.id);
                    if(pushData.Dependance == "")
                        pushData.Dependance=task.task.model.id;
                    else
                        pushData.Dependance.push(task.task.model.id);
                    console.log(pushData);
                    $.ajax({
                        url: '/fr/scheduling/api/gantt/dep/'+ pushData.id + '/',
                        type: 'PUT',
                        async:false,
                        data: pushData,
                        success: function(data){
                            console.log(data);
                        },
                        failure: function(error){
                          console.log(error);
                        }
                      });
                },
                failure: function(error){
                  console.log(error);
                }
            });
           /* var data = {'id':  data.model.to ,"Dependance":  data.task.model.id  };
            console.log(JSON.stringify(data));
            var csrftoken = getCookie('csrftoken');
            
            $.ajax({
                url: '/fr/scheduling/api/gantt/dep/'+ data.id + '/',
                type: 'PUT',
                data: data,
                success: function(data){
                    console.log(data);
                },
                failure: function(error){
                  console.log(error);
                }
              });*/
        };

        var ganttapi = function(eventName, task) {
            var csrftoken = getCookie('csrftoken');
            $.ajaxSetup({
              beforeSend: function(xhr, settings) {
                  if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                      xhr.setRequestHeader("X-CSRFToken", csrftoken);
                  }
              }
            });
            $.ajax({
                url: '/fr/scheduling/api/gantt/detail/'+ task.model.id + '/',
                type: 'PATCH',
                data: {'id':  task.model.id ,"PlannedStart": moment(task.model.from).utc().format(), "PlannedEnd":moment(task.model.to).utc().format()},
                success: function(data){
                    console.log(data);
                },
                failure: function(error){
                  console.log(error);
                }
              });
        };

        // Event handler
        var logRowEvent = function(eventName, row) {
            $log.info('[Event] ' + eventName + ': ' + row.model.name);
        };

        // Event handler
        var logTimespanEvent = function(eventName, timespan) {
            $log.info('[Event] ' + eventName + ': ' + timespan.model.name);
        };

        // Event handler
        var logLabelsEvent = function(eventName, width) {
            $log.info('[Event] ' + eventName + ': ' + width);
        };

        // Event handler
        var logColumnsGenerateEvent = function(columns, headers) {
            $log.info('[Event] ' + 'columns.on.generate' + ': ' + columns.length + ' column(s), ' + headers.length + ' header(s)');
        };

        // Event handler
        var logRowsFilterEvent = function(rows, filteredRows) {
            $log.info('[Event] rows.on.filter: ' + filteredRows.length + '/' + rows.length + ' rows displayed.');
        };

        // Event handler
        var logTasksFilterEvent = function(tasks, filteredTasks) {
            $log.info('[Event] tasks.on.filter: ' + filteredTasks.length + '/' + tasks.length + ' tasks displayed.');
        };

        // Event handler
        var logReadyEvent = function() {
            $log.info('[Event] core.on.ready');
        };

        // Event utility function
        var addEventName = function(eventName, func) {
            return function(data) {
                return func(eventName, data);
            };
        };

        // angular-gantt options
        $scope.options = {
            mode: 'custom',
            scale: 'day',
            sortMode: undefined,
            sideMode: 'Tree',
            daily: false,
            maxHeight: false,
            width: false,
            zoom: 1,
            columns: ['model.name', 'from', 'to'],
            treeTableColumns: ['from', 'to'],
            columnsHeaders: {'model.name' : 'Name', 'from': 'From', 'to': 'To'},
            columnsClasses: {'model.name' : 'gantt-column-name', 'from': 'gantt-column-from', 'to': 'gantt-column-to'},
            columnsFormatters: {
                'from': function(from) {
                    return from !== undefined ? from.format('lll') : undefined;
                },
                'to': function(to) {
                    return to !== undefined ? to.format('lll') : undefined;
                }
            },
            treeHeaderContent: '{+getHeader()+}',
            columnsHeaderContents: {
                'model.name': '{+getHeader()+}',
                'from': '{+getHeader()+}',
                'to': '{+getHeader()+}'
            },
            autoExpand: 'none',
            taskOutOfRange: 'truncate',
            fromDate: new Date(2017, 6, 10),//moment().subtract(5, 'days'),
            toDate: new Date(2017,10,15),//moment().add(90, 'days'),
            rowContent: '<i class="fa fa-align-justify"></i> {+row.model.name+}',
            taskContent : '<i class="fa fa-tasks"></i> {+task.model.name+}',
            allowSideResizing: true,
            labelsEnabled: true,
            currentDate: 'column',
            currentDateValue: moment(),
            draw: false,
            readOnly: false,
            groupDisplayMode: 'group',
            filterTask: '',
            filterRow: '',
            timeFrames: {
                'day': {
                    start: moment('08:00', 'HH:mm'),
                    end: moment('20:00', 'HH:mm'),
                    color: '#ACFFA3',
                    working: true,
                    default: true
                },
                'closed': {
                    working: false,
                    default: true
                },
                'weekend': {
                    working: false
                },
                'holiday': {
                    working: false,
                    color: 'red',
                    classes: ['gantt-timeframe-holiday']
                }
            },
            dateFrames: {
                'weekend': {
                    evaluator: function(date) {
                        return date.isoWeekday() === 6 || date.isoWeekday() === 7;
                    },
                    targets: ['weekend']
                }
            },
            timeFramesWorkingMode: 'hidden',
            timeFramesNonWorkingMode: 'cropped',
            columnMagnet: '60 minutes',
            timeFramesMagnet: true,
            dependencies: {
                enabled: true,
                conflictChecker: true,
                readonly:true
            },
            movable: {
                allowResizing:false,
                allowRowSwitching: false
            },
            corner: {
                headersLabels: function(key) {return key.charAt(0).toUpperCase() + key.slice(1);},
                headersLabelsTemplates: '{+getLabel(header)+}'
            },
            targetDataAddRowIndex: undefined,
            canDraw: false,
            api: function(api) {
                // API Object is used to control methods and events from angular-gantt.
                $scope.api = api;

                api.core.on.ready($scope, function() {
                    // Log various events to console
                    api.scroll.on.scroll($scope, logScrollEvent);
                    api.core.on.ready($scope, logReadyEvent);
                    /*
                    api.data.on.remove($scope, addEventName('data.on.remove', logDataEvent));
                    api.data.on.load($scope, addEventName('data.on.load', logDataEvent));
                    api.data.on.clear($scope, addEventName('data.on.clear', logDataEvent));
                    api.data.on.change($scope, addEventName('data.on.change', logDataEvent));
                    */
                    //api.tasks.on.add($scope, addEventName('tasks.on.add', logTaskEvent));
                    api.tasks.on.change($scope, addEventName('change', ganttapi));
                    api.tasks.on.change($scope, addEventName('change', logTaskEvent));
                    api.dependencies.on.add($scope, addEventName('add dependency', ganttapi_dependancy));
                    api.dependencies.on.remove($scope, addEventName('add dependency', ganttapi_dependancy));
                    //api.tasks.on.rowChange($scope, addEventName('tasks.on.rowChange', logTaskEvent));
                    //api.tasks.on.remove($scope, addEventName('tasks.on.remove', logTaskEvent));

                   /* if (api.tasks.on.moveBegin) {
                        api.tasks.on.moveBegin($scope, addEventName('tasks.on.moveBegin', logTaskEvent));
                        //api.tasks.on.move($scope, addEventName('tasks.on.move', logTaskEvent));
                        api.tasks.on.moveEnd($scope, addEventName('tasks.on.moveEnd', logTaskEvent));

                        api.tasks.on.resizeBegin($scope, addEventName('tasks.on.resizeBegin', logTaskEvent));
                        //api.tasks.on.resize($scope, addEventName('tasks.on.resize', logTaskEvent));
                        api.tasks.on.resizeEnd($scope, addEventName('tasks.on.resizeEnd', logTaskEvent));
                    }

                    if (api.tasks.on.drawBegin) {
                        api.tasks.on.drawBegin($scope, addEventName('tasks.on.drawBegin', logTaskEvent));
                        //api.tasks.on.draw($scope, addEventName('tasks.on.draw', logTaskEvent));
                        api.tasks.on.drawEnd($scope, addEventName('tasks.on.drawEnd', logTaskEvent));
                    }*/

                    /*api.rows.on.add($scope, addEventName('rows.on.add', logRowEvent));
                    api.rows.on.change($scope, addEventName('rows.on.change', logRowEvent));
                    api.rows.on.move($scope, addEventName('rows.on.move', logRowEvent));
                    api.rows.on.remove($scope, addEventName('rows.on.remove', logRowEvent));
                    */
                    /*
                    api.side.on.resizeBegin($scope, addEventName('labels.on.resizeBegin', logLabelsEvent));
                    //api.side.on.resize($scope, addEventName('labels.on.resize', logLabelsEvent));
                    api.side.on.resizeEnd($scope, addEventName('labels.on.resizeEnd', logLabelsEvent));

                    api.timespans.on.add($scope, addEventName('timespans.on.add', logTimespanEvent));
                    api.columns.on.generate($scope, logColumnsGenerateEvent);
                    */
                    /*
                    api.rows.on.filter($scope, logRowsFilterEvent);
                    api.tasks.on.filter($scope, logTasksFilterEvent);

                    api.data.on.change($scope, function(newData) {
                        if (dataToRemove === undefined) {
                            dataToRemove = [
                        
                            ];
                        }
                    });
                    */
                    // When gantt is ready, load data.
                    // `data` attribute could have been used too.
                    $scope.load();

                    // Add some DOM events
                    /*api.directives.on.new($scope, function(directiveName, directiveScope, element) {
                        if (directiveName === 'ganttTask') {
                            element.bind('click', function(event) {
                                event.stopPropagation();
                                logTaskEvent('task-click', directiveScope.task);
                            });
                            element.bind('mousedown touchstart', function(event) {
                                event.stopPropagation();
                                $scope.live.row = directiveScope.task.row.model;
                                if (directiveScope.task.originalModel !== undefined) {
                                    $scope.live.task = directiveScope.task.originalModel;
                                } else {
                                    $scope.live.task = directiveScope.task.model;
                                }
                                $scope.$digest();
                            });
                        } else if (directiveName === 'ganttRow') {
                            element.bind('click', function(event) {
                                event.stopPropagation();
                                logRowEvent('row-click', directiveScope.row);
                            });
                            element.bind('mousedown touchstart', function(event) {
                                event.stopPropagation();
                                $scope.live.row = directiveScope.row.model;
                                $scope.$digest();
                            });
                        } else if (directiveName === 'ganttRowLabel') {
                            element.bind('click', function() {
                                logRowEvent('row-label-click', directiveScope.row);
                            });
                            element.bind('mousedown touchstart', function() {
                                $scope.live.row = directiveScope.row.model;
                                $scope.$digest();
                            });
                        }
                    });*/
                    /*
                    api.tasks.on.rowChange($scope, function(task) {
                        $scope.live.row = task.row.model;
                    });
                    */
                    objectModel = new ObjectModel(api);
                });
            }
        };
        /*
        $scope.handleTaskIconClick = function(taskModel) {
            alert('Icon from ' + taskModel.name + ' task has been clicked.');
        };

        $scope.handleRowIconClick = function(rowModel) {
            alert('Icon from ' + rowModel.name + ' row has been clicked.');
        };
        */
        $scope.expandAll = function() {
            $scope.api.tree.expandAll();
        };

        $scope.collapseAll = function() {
            $scope.api.tree.collapseAll();
        };

        $scope.$watch('options.sideMode', function(newValue, oldValue) {
            if (newValue !== oldValue) {
                $scope.api.side.setWidth(undefined);
                $timeout(function() {
                    $scope.api.columns.refresh();
                });
            }
        });

        $scope.canAutoWidth = function(scale) {
            if (scale.match(/.*?hour.*?/) || scale.match(/.*?minute.*?/)) {
                return false;
            }
            return true;
        };

        $scope.getColumnWidth = function(widthEnabled, scale, zoom) {
            if (!widthEnabled && $scope.canAutoWidth(scale)) {
                return undefined;
            }

            if (scale.match(/.*?week.*?/)) {
                return 150 * zoom;
            }

            if (scale.match(/.*?month.*?/)) {
                return 300 * zoom;
            }

            if (scale.match(/.*?quarter.*?/)) {
                return 500 * zoom;
            }

            if (scale.match(/.*?year.*?/)) {
                return 800 * zoom;
            }

            return 40 * zoom;
        };

        // Reload data action
        $scope.load = function() {
            $http.get('/fr/scheduling/api/gantt/').then(function (response){
                var json = JSON.stringify(response.data).split('"_from":').join('"from":').split("Dependance").join("dependencies");
                json=JSON.parse(json);
                $.each(json, function(i, v) {
                   $.each(v.tasks, function (i, v){
                    v.dependencies.forEach(function (result, index, array){
                        var item = {};
                        item.from=""+result;
                        array.splice(index);
                        array.push(item);
                    });
                   });
                });
                $scope.data=json;
            });
            $scope.timespans=holidays;

        };

        $scope.reload = function() {
            $scope.load();
        };
        /*
        // Remove data action
        $scope.remove = function() {
            $scope.api.data.remove(dataToRemove);
            $scope.api.dependencies.refresh();
        };
        */
        /*
        // Clear data action
        $scope.clear = function() {
            $scope.data = [];
        };
        */
        /*
        // Add data to target row index
        $scope.addOverlapTaskToTargetRowIndex = function() {
            var targetDataAddRowIndex = parseInt($scope.options.targetDataAddRowIndex);

            if (targetDataAddRowIndex) {
                var targetRow = $scope.data[$scope.options.targetDataAddRowIndex];

                if (targetRow && targetRow.tasks && targetRow.tasks.length > 0) {
                    var firstTaskInRow = targetRow.tasks[0];
                    var copiedColor = firstTaskInRow.color;
                    var firstTaskEndDate = firstTaskInRow.to.toDate();
                    var overlappingFromDate = new Date(firstTaskEndDate);

                    overlappingFromDate.setDate(overlappingFromDate.getDate() - 1);

                    var overlappingToDate = new Date(overlappingFromDate);

                    overlappingToDate.setDate(overlappingToDate.getDate() + 7);

                    targetRow.tasks.push({
                        'name': 'Overlapping',
                        'from': overlappingFromDate,
                        'to': overlappingToDate,
                        'color': copiedColor
                    });
                }
            }
        };
*/

        // Visual two way binding.
        //$scope.live = {};
/*
        var debounceValue = 1000;

        var listenTaskJson = debounce(function(taskJson) {
            if (taskJson !== undefined) {
                var task = angular.fromJson(taskJson);
                objectModel.cleanTask(task);
                var model = $scope.live.task;
                angular.merge(model, task);
            }
        }, debounceValue);
        $scope.$watch('live.taskJson', listenTaskJson);

        var listenRowJson = debounce(function(rowJson) {
            if (rowJson !== undefined) {
                var row = angular.fromJson(rowJson);
                objectModel.cleanRow(row);
                var tasks = row.tasks;

                delete row.tasks;
                delete row.drawTask;

                var rowModel = $scope.live.row;

                angular.merge(rowModel, row);

                var newTasks = {};
                var i, l;

                if (tasks !== undefined) {
                    for (i = 0, l = tasks.length; i < l; i++) {
                        objectModel.cleanTask(tasks[i]);
                    }

                    for (i = 0, l = tasks.length; i < l; i++) {
                        newTasks[tasks[i].id] = tasks[i];
                    }

                    if (rowModel.tasks === undefined) {
                        rowModel.tasks = [];
                    }
                    for (i = rowModel.tasks.length - 1; i >= 0; i--) {
                        var existingTask = rowModel.tasks[i];
                        var newTask = newTasks[existingTask.id];
                        if (newTask === undefined) {
                            rowModel.tasks.splice(i, 1);
                        } else {
                            objectModel.cleanTask(newTask);
                            angular.merge(existingTask, newTask);
                            delete newTasks[existingTask.id];
                        }
                    }
                } else {
                    delete rowModel.tasks;
                }

                angular.forEach(newTasks, function(newTask) {
                    rowModel.tasks.push(newTask);
                });
            }
        }, debounceValue);
        $scope.$watch('live.rowJson', listenRowJson);


        $scope.$watchCollection('live.task', function(task) {
            $timeout(function() {
                $scope.live.taskJson = angular.toJson(task, true);
                $scope.live.rowJson = angular.toJson($scope.live.row, true);
            });
        });

        $scope.$watchCollection('live.row', function(row) {
            $timeout(function() {
                $scope.live.rowJson = angular.toJson(row, true);
                if (row !== undefined && row.tasks !== undefined && row.tasks.indexOf($scope.live.task) < 0) {
                    $scope.live.task = row.tasks[0];
                }
            });

        });

        $scope.$watchCollection('live.row.tasks', function() {
            $timeout(function() {
                $scope.live.rowJson = angular.toJson($scope.live.row, true);
            });
        });
*/
    }]);
