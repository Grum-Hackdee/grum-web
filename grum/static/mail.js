"use strict";

angular.module('grum', [])
    .controller('InboxController', ['$scope','$http', 'NotificationService', function($scope, $http, NotificationService) {
        $scope.emails = [];
        $scope.focus_mail = {};
        $scope.focusEmail = function(index) {
            // get email, and focus
            $http.get('/api/messages/' + $scope.emails[index].id)
                .success(function(data, success, headers, config) {
                    $scope.emails[index].read = true;
                    $scope.focus_mail = data['message'];
                    $("#focus_email").modal();
                })
                .error(function(data, success, headers, config) {
                    $scope.error = "Could not access Message " + email.id
                    Raven.captureMessage($scope.error);
                })
        }

        var updateScope = function() {
            for (var i = 0; i < $scope.emails.length; i++) {
                $scope.emails[i].fromnow = moment($scope.emails[i].timestamp * 1000).fromNow();
                $scope.emails[i].f_fromnow = moment($scope.emails[i].timestamp * 1000).fromNow;
                // $scope.emails[i].gravatar = "";
                $scope.emails[i].gravatar = 'http://www.gravatar.com/avatar/' + md5($scope.emails[i].from_raw) + "?s=32"
            }
        }
        var checkEmail = function() {
            $http.get('/api/inbox')
                .success(function(data, status, headers, config) {
                    $scope.emails = data['inbox'].reverse();
                    updateScope();
                })
                .error(function(data, status, headers, config) {
                    $scope.error = "Could not update emails, please try again later and check your connection."
                    Raven.captureMessage($scope.error);
                })
                .finally()
                    }


        
        checkEmail();
        NotificationService.onTimeAgo($scope, checkEmail);
        $scope.getEmail = Raven.context(function() { checkEmail(); });
    }])
    .factory('NotificationService', ['$rootScope', function($rootScope) {
        var TIME_AGO_TICK = "e:timAgo";
        var timeAgoTick = function() {
            $rootScope.$broadcast(TIME_AGO_TICK);
        }

        setInterval(function() {
            timeAgoTick();
            $rootScope.$apply();
        }, 1000 * 60);
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
