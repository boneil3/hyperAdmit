/**
 * Created by brendan on 4/18/15.
 */

hyperApp.controller('signupCtrl', function ($scope, $window, $timeout, signupService) {
    var vm = this;

    $scope.signup = function (user) {
        signupService.signup(user);
    };

});

hyperApp.factory('signupService', function ($http, $window, $timeout, $location, crypto, GApi, sessionService) {
  $http.defaults.useXDomain = true;
  $http.defaults.headers.common["Accept"] = "application/json";
  $http.defaults.headers.common["Content-Type"] = "application/json";

  return {
    signup: function (user, scope) {
        var base_url = $window.location.host;
        var api_url = '';
        if (base_url.indexOf('localhost') > -1) {
            api_url = 'http://localhost:8080/api/signup';
        }
        else {
            api_url = 'https://centralparkedu.appspot.com/api/signup';
        }

        var s_user = {
            'email': user.email,
            'password': crypto.hash(user.password),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone
        };
        var $promise = $http.post(api_url, s_user); //send data over to server
        $promise.then(function (msg) {
            console.log(msg.data);
            user.problem = msg;
            if (msg.data.code == 200) {
                sessionService.set('token', msg.data.response.token);
                sessionService.set('user_id', msg.data.response.user_id);
                $location.path('/officers');
            }
            else if (msg.data.code >= 400) {
                user.email = 'email_taken@sod.com';
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
    }
  };
});