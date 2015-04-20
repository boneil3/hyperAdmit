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
            controller: 'adOffCtrl',
            controllerAs: 'vm'
        })
        .when('/home', {
            templateUrl: 'home'
        })
        .otherwise({
            redirectTo: '/home'
        });
}]);
hyperApp.factory('AdmissionOfficer', ['$resource', function ($resource) {
    var AdmissionOfficer = $resource('http://localhost:8080/_ah/api/hyperadmit/v1/adoffs/:id', {id: '@id'}, {
        'get': {method: 'GET'},
        'update': {method: 'POST'}
    });
    AdmissionOfficer.add = $resource('http://localhost:8080/_ah/api/hyperadmit/v1/insertadoff', {}, {
        'insert': {method: 'POST'}
    });
    AdmissionOfficer.list = $resource('http://localhost:8080/_ah/api/hyperadmit/v1/getadoff', {pageToken: '@pageToken'}, {
        'query': {method: 'GET', isArray: false}
    });
    return AdmissionOfficer
}]);

hyperApp.controller('adOffCtrl', ['$scope', '$window', '$timeout', 'GApi', 'AdmissionOfficer', function ($scope, $window, $timeout, GApi, AdmissionOfficer) {
    var vm = this;
        vm.ad_offs = [];
        vm.lastPageToken = '';
        vm.dropOne = ['Undergrad', 'Business', 'Law', 'Medical'];
        vm.dropTwo = ['Ivy', 'Top 20', 'Top 40'];
        vm.dropThree = ['@fat', '@mdo'];
        vm.dropdownSelected = ['', 'Top 40', ''];
        vm.alerts = [];

    $timeout(function() {
        AdmissionOfficer.list.query({order: '-joined', pageToken: ''}, function (response) {
            if (response.code >= 400) {
                //error
            }
            else {
                angular.forEach(response.items, function (item) {
                    var ad_off = new AdmissionOfficer();
                        ad_off.college_rank = item.college_rank;
                        ad_off.hours_consulted = item.hours_consulted;
                        ad_off.howcanihelp = item.howcanihelp;
                        ad_off.whoami = item.whoami;
                        ad_off.job_title = item.job_title;
                        ad_off.knowledge_areas = item.knowledge_areas;
                        ad_off.last_active = item.last_active;
                        ad_off.location = item.location;
                        ad_off.school = item.school;
                        ad_off.school_type = item.school_type;
                        ad_off.verified = item.verified;
                        ad_off.whoami = item.whoami;
                    vm.ad_offs.push(ad_off);
                });
                $timeout(function() {
                    vm.lastPageToken = response.nextPageToken;
                }, 100);
            }
        });
    }, 3000);

    vm.dropdownSelect = function (item, ddNum) {
        if (vm.dropdownSelected[ddNum] != item) {
            var alert = {};
                alert.msg = item;
                alert.type = 'success';
            vm.alerts.push(alert);

            vm.dropdownSelected[ddNum] = item;
            AdmissionOfficer.list.query({
                'school_type': vm.dropdownSelected[0],
                'college_rank': vm.dropdownSelected[1]
            }, function (response) {
                if (response.code >= 400) {
                    //error
                }
                else {
                    vm.ad_offs = [];
                    angular.forEach(response.items, function (item) {
                        var ad = new AdmissionOfficer();
                            ad.id = item.id;
                            ad.alias = item.alias;
                            ad.school = item.school;
                            ad.location = item.location;
                            ad.rating = item.rating;
                            ad.hours_consulted = item.hours_consulted;
                            ad.last_active = item.last_active;
                            ad.knowledge_areas = item.knowledge_areas;
                            ad.whoami = item.whoami;
                            ad.howcanihelp = item.howcanihelp;
                            ad.job_title = item.job_title;
                        vm.ad_offs.push(ad);
                    });
                    $timeout(function() {
                        vm.searchView = true;
                    }, 100);
                }
            });
        }
    };

    vm.get_more_adoffs = function() {
        AdmissionOfficer.list.query({'pageToken': vm.lastPageToken}, function (response) {
            if (response.code >= 400) {
            //error
            }
            else {
                angular.forEach(response.items, function (item) {
                    var ad_off = new AdmissionOfficer();
                        ad_off.college_rank = item.college_rank;
                        ad_off.hours_consulted = item.hours_consulted;
                        ad_off.howcanihelp = item.howcanihelp;
                        ad_off.whoami = item.whoami;
                        ad_off.job_title = item.job_title;
                        ad_off.knowledge_areas = item.knowledge_areas;
                        ad_off.last_active = item.last_active;
                        ad_off.location = item.location;
                        ad_off.school = item.school;
                        ad_off.school_type = item.school_type;
                        ad_off.verified = item.verified;
                        ad_off.whoami = item.whoami;
                    vm.ad_offs.push(ad_off);
                });
                $timeout(function() {
                    vm.lastPageToken = response.nextPageToken;
                }, 100);
            }
        });
    };
    vm.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };
    vm.addAdOff = function (email) {
        var now = moment().format('YYYY-MM-DDTHH:mm:ss');
        AdmissionOfficer.add.insert({
            'email': email,
            'first_name': 'bob',
            'last_name': 'whatever',
            'phone': '0404040',
            'id': '',
            'verified': false,
            'school': '',
            'school_type': '',
            'location': '',
            'rating': 5,
            'hours_consulted': 0,
            'last_active': now + '.0000',
            'knowledge_areas': '',
            'whoami': '',
            'howcanihelp': '',
            'job_title': '',
            'college_rank': 0
        }, function (response) {
            if (response.code >= 400) {
                // error
            }
            else {
                var adOff = new AdmissionOfficer();
                    adOff.id = response.id;
                    adOff.verified = response.verified;
                    adOff.school = response.school;
                    adOff.school_type = response.school_type;
                    adOff.location = response.location;
                    adOff.rating = response.rating;
                    adOff.hours_consulted = response.hours_consulted;
                    adOff.last_active = response.last_active;
                    adOff.knowledge_areas = response.knowledge_areas;
                    adOff.whoami = response.whoami;
                    adOff.howcanihelp = response.howcanihelp;
                    adOff.job_title = response.job_title;
                    adOff.college_rank = response.college_rank;
                    adOff.alias = response.alias;
                $timeout(function() {
                    vm.ad_offs.push(adOff);
                }, 100);
            }
        });
    };
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
    var base = 'https://centralparkedu.appspot.com/_ah/api/';
    GApi.load('hyperadmit', 'v1', base);
    GApi.load('plus', 'v1');
    GApi.load('oauth2', 'v2');

    var routespermission = ['/login'];

    $rootScope.$on('$routeChangeStart', function () {
        if (routespermission.indexOf($location.path()) !== 1 && !loginService.isLogged() && $location.path() !== '/signup' && $location.path() !== '/reset') {
            $location.path('/home');
        }
    });
}]);