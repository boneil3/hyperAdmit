/**
 * Created by brendan on 4/18/15.
 */

hyperApp.controller('checkoutCtrl', function ($location, $scope, $window, logoutService, GApi, sessionService) {
    var vm = this;
        vm.token = '';
    $window.Stripe.setPublishableKey('YOUR-KEY-COMES-HERE');

    $scope.logout = function (user) {
        logoutService.login(user, $scope);
    };
    $scope.stripeCallback = function (code, result) {
        if (result.error) {
            window.alert('it failed! error: ' + result.error.message);
        } else {
            GApi.execute('centralparkedu', 'hyperadmit.process_payment', {
                'user_id': sessionService.get('user_id'),
                'user_token': sessionService.get('token'),
                'stripeCardId': result.id,
                'purchase_type': vm.purchase_type
            }).then(function (response) {
                if (response.code >= 400) {
                    //error
                }
                else {
                    //completed purchase
                    $location.path('google.com');
                }
            });
        }
    };
});