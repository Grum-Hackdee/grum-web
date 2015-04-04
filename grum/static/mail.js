"use strict";

angular.module('grum', [])
    .controller('InboxController', ['$scope','$http', function($scope, $http) {
        $scope.emails = [];

        var checkEmail = function() {
            $http.get('/api/inbox')
                .success(function(data, status, headers, config) {
                    $scope.emails = data['inbox'];
                })
                .error(function(data, status, headers, config) {
                    $scope.error = "Could not update emails, please try again later and check your connection."
                })
                .finally()
        }
        checkEmail();
        $scope.getEmail = Raven.context(function() { checkEmail(); });
    }]);
