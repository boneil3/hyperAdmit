/**
 * Created by brendan on 4/22/15.
 */
hyperApp.controller('homeCtrl', function ($location, $scope, $window, $timeout, $modal, GApi, sessionService) {
    var vm = this;

    vm.openModal = function() {
        var modalInstance = $modal.open({
            templateUrl: 'static/html/freeTrial.html',
            controller: 'freeTrialCtrl',
            controllerAs: 'vm',
            size: 'lg'
        });
    }
});