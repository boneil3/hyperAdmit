var hyperApp = angular.module('hyperApp', ['ngResource', 'ngRoute', 'ui.bootstrap', 'angular-google-gapi']);

hyperApp.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/signup', {
            templateUrl: 'signup',
            controller: 'signupCtrl',
            controllerAs: 'vm'
        })
        .when('/login', {
            templateUrl: 'login',
            controller: 'loginCtrl',
            controllerAs: 'vm'
        })
        .when('/checkout', {
            templateUrl: 'checkout',
            controller: 'checkoutCtrl',
            controllerAs: 'vm'
        })
        .when('/officers', {
            templateUrl: 'officers',
            controller: 'officerListCtrl',
            controllerAs: 'vm'
        })
        .when('/home', {
            templateUrl: 'home',
            controller: 'homeCtrl',
            controllerAs: 'vm'
        })
        .when('/about', {
            templateUrl: 'about',
            controller: 'aboutCtrl',
            controllerAs: 'vm'
        })
        .otherwise({
            redirectTo: '/home'
        });
}]);
hyperApp.factory('AdmissionsOfficer', ['$resource', function ($resource) {
    //var AdmissionsOfficer = $resource('https://centralparkedu.appspot.com/_ah/api/centralparkedu/v1/hyperadmit/adoffs/:id', {id: '@id'}, {

    var AdmissionsOfficer = $resource('http://localhost:8080/_ah/api/centralparkedu/v1/hyperadmit/adoffs/:id', {id: '@id'}, {
        'get': {method: 'GET'},
        'update': {method: 'POST'}
    });
    //AdmissionsOfficer.add = $resource('https://centralparkedu.appspot.com/_ah/api/centralparkedu/v1/hyperadmit/insertadoff', {}, {
    AdmissionsOfficer.add = $resource('http://localhost:8080/_ah/api/centralparkedu/v1/hyperadmit/insertadoff', {}, {
        'insert': {method: 'POST'}
    });
    //AdmissionsOfficer.list = $resource('https://centralparkedu.appspot.com/_ah/api/centralparkedu/v1/hyperadmit/getadoffs', {pageToken: '@pageToken'}, {
    AdmissionsOfficer.list = $resource('http://localhost:8080/_ah/api/centralparkedu/v1/hyperadmit/getadoffs', {pageToken: '@pageToken'}, {

        'query': {method: 'GET', isArray: false}
    });
    return AdmissionsOfficer
}]);

hyperApp.factory('crypto', function () {
    return {
        hash: function (value) {
            return CryptoJS.SHA256(value).toString();
        }
    };
});
hyperApp.factory('sessionService', ['$http', function ($http) {
  return {
    set: function (key, value) {
      return sessionStorage.setItem(key, value);
    },
    get: function (key) {
      return sessionStorage.getItem(key);
    },
    destroy: function (key) {
      return sessionStorage.removeItem(key);
    }
  };
}]);
hyperApp.run(['$window', 'GApi', '$rootScope', '$location', 'loginService', function ($window, GApi, $rootScope, $location, loginService) {
    var base_url = $window.location.host;
    var api_url = '';
    if (base_url.indexOf('localhost') > -1) {
        api_url = 'http://localhost:8080/_ah/api';
    }
    else {
        api_url = 'https://centralparkedu.appspot.com/_ah/api';
    }

    GApi.load('centralparkedu', 'v1', api_url);
    GApi.load('plus', 'v1');
    GApi.load('oauth2', 'v2');

    $rootScope.$on('$routeChangeStart', function () {
        if ($location.path() !== '/login' && !loginService.isLogged() && $location.path() !== '/signup' && $location.path() !== '/reset' && $location.path() !== '/home' && $location.path() !== '/about') {
            $location.path('/home');
        }
    });
}]);