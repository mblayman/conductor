/* jshint node: true */

module.exports = function(deployTarget) {
  var ENV = {
    build: {},
    cp: {},
    'revision-data': {type: 'git-commit'}
  };

  if (deployTarget === 'development') {
    ENV.build.environment = 'development';
    ENV.cp.destDir = 'tmp/cp-deploy';
  }

  if (deployTarget === 'staging') {
    ENV.build.environment = 'production';
    // configure other plugins for staging deploy target here
  }

  if (deployTarget === 'production') {
    ENV.build.environment = 'production';
    ENV.cp.destDir = 'tmp/cp-prod-deploy';
  }

  // Note: if you need to build some configuration asynchronously, you can return
  // a promise that resolves with the ENV object instead of returning the
  // ENV object synchronously.
  return ENV;
};
