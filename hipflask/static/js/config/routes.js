(function () {
  'use strict';

  function configureRoutes ($stateProvider) {

    function template (path) {
      return 'static/partials' + path;
    }

    /*
    var league = {
      name:        'league',
      url:         '/league',
      templateUrl: template('/league.html')
    };
    $stateProvider.state(league);
    */
  }

  function fallbackRoute ($urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
  }

  angular.module('Hipflask')
    .config(['$stateProvider', configureRoutes])
    .config(['$urlRouterProvider', fallbackRoute]);
}());
