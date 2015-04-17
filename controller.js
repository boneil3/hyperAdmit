angular.module('hyperApp', ['ngResource', 'ngRoute', 'ui.bootstrap', 'angular-google-gapi'])

hyperApp.factory('AdmissionOfficer', ['$resource', function ($resource) {
    var AdmissionOfficer = $resource('https://centralparkedu.appspot.com/_ah/api/hyperadmit/v1/adoffs/:id', {id: '@id'}, {
        'get': {method: 'GET'},
        'update': {method: 'POST'}
    });
    AdmissionOfficer.list = $resource('https://centralparkedu.appspot.com/_ah/api/hyperadmit/v1/getadoff', {}, {
        'query': {method: 'GET', isArray: false}
    });
    return AdmissionOfficer
}]);

hyperApp.controller('adOffCtrl', ['$scope', '$window', '$timeout', 'GApi', 'AdmissionOfficer', function ($scope, $window, $timeout, GApi, AdmissionOfficer) {
    var vm = this;
        vm.ad_offs = [];
        vm.lastPageToken = '';
        vm.dropOne = ['Undergrad', 'Business', 'Law', 'Medical']
        vm.dropTwo = ['Ivy', 'Top 20', 'Top 40']
        vm.dropThree = ['@fat', '@mdo']
        vm.dropdownSelected = ['', '', ''];
        vm.searchView = false;

    AdmissionOfficer.list.query({'pageToken': vm.lastPageToken}, function (response) {
        if (response.code >= 400) {
        //error
        }
        else {
            angular.forEach(response.items, function (item) {
                vm.ad_offs.push(item);
            });
        }
    });

    GApi.execute('centralparkedu', 'hyperadmit.get_all_adOffs').then(function (response) {
        if (response.code >= 400) {
            //error
        }
        else {
            angular.forEach(response.items, function (item) {
                vm.ad_offs.push(item);
            });
        }
    });
    vm.dropdownSelect = function (item, ddNum) {
        if (vm.dropdownSelected[ddNum] != item) {
            vm.dropdownSelected[ddNum] = item;
            AdmissionOfficer.list.query({
                'school_type': vm.dropdownSelected[0],
                'college_rank': vm.dropdownSelected[1]
            }, function (response) {
                if (response.code >= 400) {
                    //error
                }
                else {
                    vm.searchOfficers = [];
                    angular.forEach(response.items, function (item) {
                        ad = new AdmissionOfficer();
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
                        vm.searchOfficers.push(ad);
                    });
                    $timeout(function() {
                        vm.searchView = true;
                    }, 100);
                }
            });
        }
    };
    vm.typeaheadSelect = function (item) {
        AdmissionOfficer.get({'id': item.id}, function (response) {
            if (response.code >= 400) {
                //error
            }
            else {
                vm.searchOfficers = [];
                ad = new AdmissionOfficer();
                    ad.id = response.id;
                    ad.alias = response.alias;
                    ad.school = response.school;
                    ad.location = response.location;
                    ad.rating = response.rating;
                    ad.hours_consulted = response.hours_consulted;
                    ad.last_active = response.last_active;
                    ad.knowledge_areas = response.knowledge_areas;
                    ad.whoami = response.whoami;
                    ad.howcanihelp = response.howcanihelp;
                    ad.job_title = response.job_title;
                $timeout(function() {
                    vm.searchView = true;
                    vm.searchOfficers.push(ad);
                }, 100);
            }
        });
    };
    vm.get_more_adoffs = function() {
        AdmissionOfficer.list.query({'pageToken': vm.lastPageToken}, function (response) {
            if (response.code >= 400) {
            //error
        }
            else {
                angular.forEach(response.items, function (item) {
                    vm.ad_offs.push(item);
                });
            }
        });
    };
}]);

hyperApp.run(['$scope', '$window', 'GApi', function ($scope, $window, GApi) {
    var base = 'https://centralparkedu.appspot.com/_ah/api/'
    GApi.load('hyperadmit', 'v1', base);
    GApi.load('plus', 'v1');
    GApi.load('oauth2', 'v2');
}]);