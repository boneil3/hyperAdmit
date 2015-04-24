/**
 * Created by brendan on 4/23/15.
 */

hyperApp.controller('freeTrialCtrl', function ($location, $scope, $window, $modalInstance, GApi, sessionService) {

    var vm = this;
        vm.user = {};
        vm.schoolTypes = ['undergrad', 'business', 'law', 'medical'];

    vm.submitFreeTrial = function (user) {
        GApi.execute('centralparkedu', 'hyperadmit.free_trial_signup', {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'school_type': user.school_type
        }).then(function (response) {
            if (response.code >= 400) {
                window.alert('Error Processing Request!');
            }
            else {
                sessionService.set('email', response.email);
                $modalInstance.dismiss('signed up!');
                $location.path('/finishTrial');
            }
        });
    };

    vm.sendEmail = function() {
        GApi.execute('centralparkedu', 'hyperadmit.send_email').then(function (response) {
            //
        });
    };

    $scope.cancel = function() {
        $modalInstance.dismiss('closed');
    };
});