/**
 * Created by brendan on 4/18/15.
 */

hyperApp.controller('loginCtrl', function ($scope, loginService) {

    $scope.login = function (user) {
        loginService.login(user, $scope);
    };

});
hyperApp.factory('loginService', function ($http, $location, $window, $timeout, sessionService, gapiService, GApi, crypto) {

  return {

    login: function (user, scope) {
        GApi.execute('centralparkedu', 'hyperadmit.auth_user', {
            'email': user.email,
            'password': crypto.hash(user.password)
        }).then(function (response) {
            sessionService.set('user_id', response.id);
            sessionService.set('user_name', response.full_name);
            sessionService.set('token', response.msg);
            $timeout(function() {
                sessionService.set('user_id', response.id);
                sessionService.set('user_name', response.full_name);
                sessionService.set('token', response.msg);
                $location.path('/home');
            }, 500);
        });
    },
    isLogged: function () {
      if (sessionService.get('user_id')) {
        return true;
      }
    }
  };
});