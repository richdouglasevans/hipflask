(function () {
  'use strict';

  function acceptHeader ($log, $http) {
    var mimeTypes = [
      'application/json',
      'text/html;q=0.9',
      'application/xhtml+xml;q=0.9',
      '*/*;q=0.8'
    ];
    var headerValue = mimeTypes.join(',');
    $log.debug('Configuring HTTP Accept header [' + headerValue + '].');
    $http.defaults.headers.common['Accept'] = headerValue;
  }

  angular
    .module('Hipflask')
    .run(['$log', '$http', acceptHeader]);
}());
