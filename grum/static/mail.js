"use strict";

angular.module('grum', [])
    .service('UserService', ['$rootScope', '$http', function($rootScope, $http) {
        var USER_INFO = 'USER_INFO';
        var user;
        var _user = {}

        var init = function() {
            user = window.userid;
            getInfo(function() { return window.userid; });
        }

        var getInfo = function(f) {
            if (f() === undefined) {
                setTimeout(function() { getInfo(f); }, 150)
            }
            $http.get('/api/users/' + user)
                .success(function(data, result, headers, config) {
                    _user = data['user'];
                    $rootScope.$broadcast(USER_INFO);
                })
        }

        

        init();

        return {
            loadUser: function() { getInfo(); },
            getUser: function() {  return _user; },
            onUserInformation: function($scope, handler) {
                $scope.$on(USER_INFO, function() {
                    handler();
                })
            },
        }
    }])
    .service('EmailService', ['$rootScope', '$http', function($rootScope, $http) {
        var BROADCAST = 'EMAIL_RECIEVED';
        var MESSAGE_ARRIVAL = 'MESSAGE_ARRIVED';
        var update_scope = function() {
            for (var i = 0; i < emails.length; i++) {
                emails[i].fromnow = moment(emails[i].timestamp * 1000).fromNow();
                emails[i].f_fromnow = moment(emails[i].timestamp * 1000).fromNow;
                emails[i].gravatar = 'http://www.gravatar.com/avatar/' + md5(emails[i].from_raw) + "?s=32"
            }
        }

        var check_email = function() {
            $http.get('/api/inbox?count=15')
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
            markRead: function(id) {
                $http.get('/api/messages/' + emails[id].id)
                    .success(function() {
                        emails[id].read = true;
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
            loadMessage: function(id, is_id) {

                var u_id = '';
                if (is_id) {
                    u_id = id;
                } else {
                    u_id = emails[id].id;
                }

                if (u_id in cached_messages) {
                    // we have already fetched this message.
                    // time to short-circuit.
                    emails[id].read = true;
                    emails[id].dirty = true;
                    $rootScope.$broadcast(MESSAGE_ARRIVAL, cached_messages[emails[id].id])
                    $rootScope.$broadcast(BROADCAST);
                    return;
                }
                $http.get('/api/messages/' + u_id)
                    .success(function(data, success, headers, config) {
                        // change this to a function...
                        cached_messages[data['message'].id] = data['message'];
                        $rootScope.$broadcast(MESSAGE_ARRIVAL, data['message']);
                    })

                    .error(function(data, success, headers, config) {
                        var error = "Could not access Message " + u_id
                        Raven.captureMessage(error);
                    })

                if (!is_id) {
                    setTimeout(function() {
                        emails[id].read = true;
                        $rootScope.$broadcast(BROADCAST);
                    }, 150);
                }
            }

        }

    }])
    .controller('InboxController', ['$scope','$http', '$sce', 'NotificationService', 'EmailService', function($scope, $http, $sce, NotificationService, EmailService) {
        $scope.focus_mail = {};
        $scope.renderHtml = function(html_code) {
            return $sce.trustAsHtml(html_code);
        }
        $scope.emails = EmailService.getEmail();
        $scope.getEmail = Raven.context(function() { EmailService.checkEmail(); });
        $scope.markUnread = function(id, bool) {
            EmailService.markUnread(id, bool);
        }
        $scope.markRead = function(id) { EmailService.markRead(id); }

        $scope.Sync = function() { EmailService.checkEmail(); }

        $scope.func = function() {}

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
                        var index = i
                        $http.get('/api/messages/' + $scope.emails[i].id).success(function() {
                            try {
                                $scope.emails[index].dirty = false;
                            } catch (err) {
                                Raven.captureException(err);
                            }
                        })
                    } else if ($scope.emails[i].dirty == false){
                        $http.put('/api/messages/' + $scope.emails[i].id).success(function() {
                            $scope.emails[index].dirty = false;
                        })
                    }
                }
            }
            // This happens second, so that the state of the client is preserved.
            EmailService.checkEmail();
        });
        EmailService.checkEmail();
        
    }])
    .controller('ComposeController', ['$scope', '$http', 'UserService', function($scope, $http, UserService) {
        $scope.compose = {};
        $scope.compose.to = '';
        $scope.compose.subject = '';
        $scope.compose.text = '';
        // $scope.emails = UserService.getUser().emails;
        $scope.emails = ['harry@f-t.so', 'some@other.com'];
        $scope.compose.email = 'harry@f-t.so';

        $scope.sendEmail = function() {
            $http.post('/api/accounts/' + $scope.compose.email, $scope.compose)
                .success(function() { console.log('message sent'); })
        }

        $scope.wipeCompose = function() {
            $scope.compose = {};
            $scope.compose.email = 'harry@f-t.so';
        }
        
    }])
    .factory('NotificationService', ['$rootScope', function($rootScope) {
        var TIME_AGO_TICK = "e:timeAgo";
        var timeAgoTick = function() {
            $rootScope.$broadcast(TIME_AGO_TICK);
        }

        setInterval(function() {
            timeAgoTick();
            $rootScope.$apply();
        }, 1000 * 5);
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
    .controller('NavController', ['$scope', 'EmailService', 'UserService', function($scope, EmailService, UserService) {
        $scope.emails = EmailService.getEmail();
        $scope.loadMessage = function(id, bool) { EmailService.loadMessage(id, bool) }
        $scope.user = UserService.getUser();

        
        EmailService.onEmailUpdate($scope, function() {
            $scope.emails = EmailService.getEmail();
        });
        UserService.onUserInformation($scope, function() {
            $scope.user = UserService.getUser();
            $scope.user.emails = ['harry@f-o.so', 'some@other.com'];
        })
        
        var user;
        var init = function() {
            user = window.user;
        }
        init();
    }])
