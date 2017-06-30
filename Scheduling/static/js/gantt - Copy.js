'use strict';

/**
 * @ngdoc overview
 * @name angularGanttDemoApp
 * @description
 * # angularGanttDemoApp
 *
 * Main module of the application.
 */


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

        var ganttapi_dependancy = function(eventName, data){
            console.log(data);
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
                data: {'id':  task.model.id ,"PlannedStart": moment(task.model.from).utc().format("YYYY-MM-DD"), "PlannedEnd":moment(task.model.to).utc().format("YYYY-MM-DD")},
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
            fromDate: moment(new Date(2017, 5, 1, 0, 0, 0)),
            toDate: moment(new Date(2017, 7, 1, 0, 0, 0)),
            rowContent: '<i class="fa fa-align-justify"></i> {+row.model.name+}',
            taskContent : '<i class="fa fa-tasks"></i> {+task.model.name+}',
            allowSideResizing: true,
            labelsEnabled: true,
            currentDate: 'column',
            currentDateValue: new Date(2017, 6, 13, 11, 20, 0),
            draw: false,
            readOnly: false,
            groupDisplayMode: 'group',
            filterTask: '',
            filterRow: '',
            timeFrames: {
                'day': {
                    start: moment('9:00', 'HH:mm'),
                    end: moment('18:00', 'HH:mm'),
                    color: '#ACFFA3',
                    working: true,
                    default: true
                },
                'noon': {
                    start: moment('12:00', 'HH:mm'),
                    end: moment('13:00', 'HH:mm'),
                    working: false,
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
                },
                '11-november': {
                    evaluator: function(date) {
                        return date.month() === 10 && date.date() === 11;
                    },
                    targets: ['holiday']
                }
            },
            timeFramesWorkingMode: 'hidden',
            timeFramesNonWorkingMode: 'cropped',
            columnMagnet: '1 hour',
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

                    /*$http.get('/scheduling/api/gantt/').then(function (response){
                        var json = JSON.parse(JSON.stringify(response.data).split('"_from":').join('"from":'));
                        $scope.data=json;
                    });*/

                    //$scope.data = getHttpData();

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
                /*$.each(json, function(i, v) {
                   $.each(v.tasks, function (i, v){
                    v.dependencies.forEach(function (result, index, array){
                        var item = {};
                        item.to=""+result;
                        array.splice(index);
                        array.push(item);
                    });
                   });
                });*/
                $scope.data=json;
            });
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

'use strict';

/**
 * @ngdoc service
 * @name angularGanttDemoApp.Sample
 * @description
 * # Sample
 * Service in the angularGanttDemoApp.
 */
angular.module('angularGanttDemoApp')
    .service('Sample', function Sample() {
        return {
            getSampleData: function() {
                return [
                        // Order is optional. If not specified it will be assigned automatically
                        {name: 'Milestones', height: '3em', sortable: false, drawTask: false, classes: 'gantt-row-milestone', color: '#45607D', tasks: [
                            // Dates can be specified as string, timestamp or javascript date object. The data attribute can be used to attach a custom object
                            {name: 'Kickoff', color: '#93C47D', from: '2013-10-07T09:00:00', to: '2013-10-07T10:00:00', data: 'Can contain any custom data or object'},
                            {name: 'Concept approval', color: '#93C47D', from: new Date(2013, 9, 18, 18, 0, 0), to: new Date(2013, 9, 18, 18, 0, 0), est: new Date(2013, 9, 16, 7, 0, 0), lct: new Date(2013, 9, 19, 0, 0, 0)},
                            {name: 'Development finished', color: '#93C47D', from: new Date(2013, 10, 15, 18, 0, 0), to: new Date(2013, 10, 15, 18, 0, 0)},
                            {name: 'Shop is running', color: '#93C47D', from: new Date(2013, 10, 22, 12, 0, 0), to: new Date(2013, 10, 22, 12, 0, 0)},
                            {name: 'Go-live', color: '#93C47D', from: new Date(2013, 10, 29, 16, 0, 0), to: new Date(2013, 10, 29, 16, 0, 0)}
                        ], data: 'Can contain any custom data or object'},
                        {name: 'Status meetings', tasks: [
                            {name: 'Demo #1', color: '#9FC5F8', from: new Date(2013, 9, 25, 15, 0, 0), to: new Date(2013, 9, 25, 18, 30, 0)},
                            {name: 'Demo #2', color: '#9FC5F8', from: new Date(2013, 10, 1, 15, 0, 0), to: new Date(2013, 10, 1, 18, 0, 0)},
                            {name: 'Demo #3', color: '#9FC5F8', from: new Date(2013, 10, 8, 15, 0, 0), to: new Date(2013, 10, 8, 18, 0, 0)},
                            {name: 'Demo #4', color: '#9FC5F8', from: new Date(2013, 10, 15, 15, 0, 0), to: new Date(2013, 10, 15, 18, 0, 0)},
                            {name: 'Demo #5', color: '#9FC5F8', from: new Date(2013, 10, 24, 9, 0, 0), to: new Date(2013, 10, 24, 10, 0, 0)}
                        ]},
                        {name: 'Kickoff', movable: {allowResizing: false}, tasks: [
                            {name: 'Day 1', color: '#9FC5F8', from: new Date(2013, 9, 7, 9, 0, 0), to: new Date(2013, 9, 7, 17, 0, 0),
                                progress: {percent: 100, color: '#3C8CF8'}, movable: false},
                            {name: 'Day 2', color: '#9FC5F8', from: new Date(2013, 9, 8, 9, 0, 0), to: new Date(2013, 9, 8, 17, 0, 0),
                                progress: {percent: 100, color: '#3C8CF8'}},
                            {name: 'Day 3', color: '#9FC5F8', from: new Date(2013, 9, 9, 8, 30, 0), to: new Date(2013, 9, 9, 12, 0, 0),
                                progress: {percent: 100, color: '#3C8CF8'}}
                        ]},
                        {name: 'Create concept', tasks: [
                            {name: 'Create concept', priority: 20, content: '<i class="fa fa-cog" ng-click="scope.handleTaskIconClick(task.model)"></i> {{task.model.name}}', color: '#F1C232', from: new Date(2013, 9, 10, 8, 0, 0), to: new Date(2013, 9, 16, 18, 0, 0), est: new Date(2013, 9, 8, 8, 0, 0), lct: new Date(2013, 9, 18, 20, 0, 0),
                                progress: 100, sections: {
                                    items: [
                                        {name: 'Section #1', classes:['section-1'], from: new Date(2013, 9, 10, 8, 0, 0), to: new Date(2013, 9, 13, 8, 0, 0)},
                                        {name: 'Section #2', classes:['section-2'], from: new Date(2013, 9, 13, 8, 0, 0), to: new Date(2013, 9, 15, 8, 0, 0)},
                                        {name: 'Section #3', classes:['section-3'], from: new Date(2013, 9, 15, 8, 0, 0), to: new Date(2013, 9, 16, 18, 0, 0)}
                                    ]
                                }
                            }
                        ]},
                        {name: 'Finalize concept', tasks: [
                            {id: 'Finalize concept', name: 'Finalize concept', priority: 10, color: '#F1C232', from: new Date(2013, 9, 17, 8, 0, 0), to: new Date(2013, 9, 18, 18, 0, 0),
                                progress: 100}
                        ]},
                        {name: 'Development', children: ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4'], content: '<i class="fa fa-file-code-o" ng-click="scope.handleRowIconClick(row.model)"></i> {{row.model.name}}'},
                        {name: 'Sprint 1', tooltips: false, tasks: [
                            {id: 'Product list view', name: 'Product list view', color: '#F1C232', from: new Date(2013, 9, 21, 8, 0, 0), to: new Date(2013, 9, 25, 15, 0, 0),
                                progress: 25, dependencies: [{to: 'Order basket'}, {from: 'Finalize concept'}]}
                        ]},
                        {name: 'Sprint 2', tasks: [
                            {id: 'Order basket', name: 'Order basket', color: '#F1C232', from: new Date(2017, 6, 28, 8, 0, 0), to: new Date(2017,7, 1, 15, 0, 0),
                                dependencies: {to: 'Checkout'} }
                        ]},
                        {name: 'Sprint 3', tasks: [
                            {id: 'Checkout', name: 'Checkout', color: '#F1C232', from: new Date(2017,7, 4, 8, 0, 0), to: new Date(2017,7, 8, 15, 0, 0),
                                dependencies: {to: 'Login & Signup & Admin Views'} }
                        ]},
                        {name: 'Sprint 4', tasks: [
                            {id: 'Login & Signup & Admin Views', name: 'Login & Signup & Admin Views', color: '#F1C232', from: new Date(2017,7, 11, 8, 0, 0), to: new Date(2017,7, 15, 15, 0, 0),
                                dependencies: []}
                        ]},
                        {name: 'Hosting'},
                        {name: 'Setup', tasks: [
                            {id: 'HW', name: 'HW', color: '#F1C232', from: new Date(2017,7, 18, 8, 0, 0), to: new Date(2017,7, 18, 12, 0, 0)}
                        ]},
                        {name: 'Config', tasks: [
                            {id: 'SW / DNS/ Backups', name: 'SW / DNS/ Backups', color: '#F1C232', from: new Date(2017,7, 18, 12, 0, 0), to: new Date(2017,7, 21, 18, 0, 0)}
                        ]},
                        {name: 'Server', parent: 'Hosting', children: ['Setup', 'Config']},
                        {name: 'Deployment', parent: 'Hosting', tasks: [
                            {name: 'Depl. & Final testing', color: '#F1C232', from: new Date(2017,7, 21, 8, 0, 0), to: new Date(2017,7, 22, 12, 0, 0), 'classes': 'gantt-task-deployment'}
                        ]},
                        {name: 'Workshop', tasks: [
                            {name: 'On-side education', color: '#F1C232', from: new Date(2017,7, 24, 9, 0, 0), to: new Date(2017,7, 25, 15, 0, 0)}
                        ]},
                        {name: 'Content', tasks: [
                            {name: 'Supervise content creation', color: '#F1C232', from: new Date(2017,7, 26, 9, 0, 0), to: new Date(2017,7, 29, 16, 0, 0)}
                        ]},
                        {name: 'Documentation', tasks: [
                            {name: 'Technical/User documentation', color: '#F1C232', from: new Date(2017,7, 26, 8, 0, 0), to: new Date(2017,7, 28, 18, 0, 0)}
                        ]}
                    ];
            },
            getSampleTimespans: function() {
                return [
                        /*{
                            from: new Date(2017, 6, 21, 8, 0, 0),
                            to: new Date(2017, 6, 25, 15, 0, 0),
                            name: 'Sprint 2 Timespan'
                            //priority: undefined,
                            //classes: [],
                            //data: undefined
                        }*/
                    ];
            }
        };
    })
;