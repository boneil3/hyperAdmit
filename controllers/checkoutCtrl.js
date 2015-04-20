/**
 * Created by brendan on 4/18/15.
 */

hyperApp.controller('checkoutCtrl', function ($scope, logoutService) {

    $scope.logout = function (user) {
        logoutService.login(user, $scope);
    };

});