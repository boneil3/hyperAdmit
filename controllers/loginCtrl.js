/**
 * Created by brendan on 4/18/15.
 */

hyperApp.controller('loginCtrl', function ($scope, loginService) {

    $scope.login = function (user) {
        loginService.login(user, $scope);
    };

});
hyperApp.factory('loginService', function ($http, $location, $window, $timeout, sessionService, GApi, crypto) {

  return {

    login: function (user, scope) {
        var base_url = $window.location.host;
        var api_url = '';
        if (base_url.indexOf('localhost') > -1) {
            api_url = 'http://localhost:8080/api/login';
        }
        else {
            api_url = 'https://centralparkedu.appspot.com/api/login';
        }
        var s_user = {
            'email': user.email,
            'password': crypto.hash(user.password)
        };
        var $promise = $http.post(api_url, s_user);
        $promise.then(function (msg) {
        console.log(msg.data);
        user.problem = msg;
        if (msg.data.code == 200) {
          sessionService.set('token', msg.data.response.token);
          sessionService.set('user_id', msg.data.response.user_id);
          $location.path('/officers');
        }
        else if (msg.data.code >= 400) {
          sessionService.destroy('token');
          sessionService.destroy('user_id');
        }
        else {
          sessionService.destroy('token');
          sessionService.destroy('user_id');
        }
      }, function error(msg) {
        console.error(msg.message);
        scope.error = msg.message;
        sessionService.destroy('token');
        sessionService.destroy('user_id');
      });
    },
    isLogged: function () {
      if (sessionService.get('token')) {
        return true;
      }
    }
  };
});