/* jshint node: true */

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'client',
    environment: environment,
    baseURL: '/',
    locationType: 'auto',

    // TODO: check on simple auth and token settings.
    'ember-simple-auth': {},

    'ember-simple-auth-token': {
      serverTokenEndpoint: 'http://localhost:8080/api-token-auth/',
      identificationField: 'username',
      passwordField: 'password',
      tokenPropertyName: 'token',
      authorizationPrefix: 'Bearer ',
      authorizationHeaderName: 'Authorization',
      headers: {},
      refreshAccessTokens: true,
      serverTokenRefreshEndpoint: '/api-token-refresh/',
      tokenExpireName: 'exp',
      refreshLeeway: 300,
      timeFactor: 1
    },

    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    }
  };

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.baseURL = '/';
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {

  }

  return ENV;
};
