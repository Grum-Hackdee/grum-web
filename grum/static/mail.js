"use strict";

angular.module('grum', [])
    .service('EmailService', ['$rootScope', '$http', function($rootScope, $http) {
        var BROADCAST = 'EMAIL_RECIEVED';
        var MESSAGE_ARRIVAL = 'MESSAGE_ARRIVED';
        var update_scope = function() {
            for (var i = 0; i < emails.length; i++) {
                emails[i].fromnow = moment(emails[i].timestamp * 1000).fromNow();
                emails[i].f_fromnow = moment(emails[i].timestamp * 1000).fromNow;
                // emails[i].gravatar = "";
                emails[i].gravatar = 'http://www.gravatar.com/avatar/' + md5(emails[i].from_raw) + "?s=32"
            }
        }

        var check_email = function() {
            $http.get('/api/inbox')
                .success(function(data, status, headers, config) {
                    emails = data['inbox'].reverse();
                    update_scope();
                    $rootScope.$broadcast(BROADCAST);
                })
                .error(function(data, status, headers, config) {
                    error = "Could not update emails, please try again later and check your connection."
                    Raven.captureMessage(error);
                })
        }
        var emails = [];
        var cached_messages = {};
        
        return {
            updateScope: function() { update_scope(); },
            checkEmail: function() { check_email(); },
            getEmail: function() { if(emails.length == 0) check_email(); return emails; },
            markUnread: function(id) {
                // put to messages/id

                $http.put('/api/messages/' + id)
                    .success(function(data, success, headers, config) {
                        for (var i = 0; i < emails.length; i++) {
                            if (emails[i].id === id) {
                                emails[i].read = false;
                                break;
                            }
                        }
                        $rootScope.$broadcast(BROADCAST);
                    })
            },
            onEmailUpdate: function($scope, handler) {
                $scope.$on(BROADCAST, function() {
                    handler();
                })
            },
            onMessageArrival: function($scope, handler) {
                $scope.$on(MESSAGE_ARRIVAL, function(event, args) {
                    handler(event, args);
                })
            },
            loadMessage: function(id) {

                if (emails[id].id in cached_messages) {
                    // we have already fetched this message.
                    // time to short-circuit.
                    emails[id].read = true;
                    emails[id].dirty = true;
                    $rootScope.$broadcast(MESSAGE_ARRIVAL, cached_messages[emails[id].id])
                    $rootScope.$broadcast(BROADCAST);
                    return;
                }
                $http.get('/api/messages/' + emails[id].id)
                    .success(function(data, success, headers, config) {
                        // change this to a function...
                        cached_messages[data['message'].id] = data['message'];
                        $rootScope.$broadcast(MESSAGE_ARRIVAL, data['message']);
                    })

                    .error(function(data, success, headers, config) {
                        var error = "Could not access Message " + emails[id].id
                        Raven.captureMessage(error);
                    })

                setTimeout(function() {
                    emails[id].read = true;
                    $rootScope.$broadcast(BROADCAST);
                }, 150);
            }

        }

    }])
    .controller('InboxController', ['$scope','$http', 'NotificationService', 'EmailService', function($scope, $http, NotificationService, EmailService) {
        $scope.focus_mail = {};
        $scope.emails = EmailService.getEmail();
        $scope.getEmail = Raven.context(function() { EmailService.checkEmail(); });
        $scope.markUnread = function(id, bool) {
            EmailService.markUnread(id, bool);
        }

        $scope.focusEmail = function(index) {
            // get email, and focus
            EmailService.loadMessage(index);
        }

        EmailService.onEmailUpdate($scope, function() {
            $scope.emails = EmailService.getEmail();
        });
        EmailService.onMessageArrival($scope, function(event, args) {
            $scope.focus_mail = args;
            $("#focus_email").modal();
        });


        NotificationService.onTimeAgo($scope, function() {
            for (var i = 0; i < $scope.emails.length; i++) {
                if ($scope.emails[i].dirty == true) {
                    if ($scope.emails[i].read === true) {
                        // HACK: THIS NEEDS TO BE FIXED
                        // marking as read on the server.
                        $http.get('/api/messages/' + $scope.emails[i].id);
                    } else {
                        $http.put('/api/messages/' + $scope.emails[i].id);
                    }
                    $scope.emails[i].dirty = false;
                }
            }
            EmailService.checkEmail();
        });
        EmailService.checkEmail();
        
    }])
    .factory('NotificationService', ['$rootScope', function($rootScope) {
        var TIME_AGO_TICK = "e:timeAgo";
        var timeAgoTick = function() {
            $rootScope.$broadcast(TIME_AGO_TICK);
        }

        setInterval(function() {
            timeAgoTick();
            $rootScope.$apply();
        }, 1000 * 10);
        return {
            // publish
            timeAgoTick: timeAgoTick,
            // subscribe
            onTimeAgo: function($scope, handler) {
                $scope.$on(TIME_AGO_TICK, function() {
                    handler();
                });
            }
        };

    }])
