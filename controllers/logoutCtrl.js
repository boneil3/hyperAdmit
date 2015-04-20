/**
 * Created by brendan on 4/20/15.
 */

hyperApp.controller('logoutCtrl', function ($scope, logoutService) {

  $scope.message = '';

  $scope.logout = function (user) {
    logoutService.logout(user, $scope); //call logout service
  };
});

hyperApp.factory('logoutService', function ($http, $location, sessionService) {

  $http.defaults.useXDomain = true;

  return {
    logout: function (user, scope) {
        sessionService.destroy('user_id');
        sessionService.destroy('token');
        $location.path('/home');
    }
  };
});