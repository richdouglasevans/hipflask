(function (context) {
  'use strict';

  function exposeLoDash () {
    return context._.noConflict();
  }

  angular
    .module('LoDash', [])
    .constant('_', exposeLoDash());
}(window));
