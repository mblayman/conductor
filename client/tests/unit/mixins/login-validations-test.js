import EmberObject from '@ember/object';
import LoginValidationsMixin from 'client/mixins/login-validations';
import { module, test } from 'qunit';

module('Unit | Mixin | login validations');

// Replace this with your real tests.
test('it works', function(assert) {
  let LoginValidationsObject = EmberObject.extend(LoginValidationsMixin);
  let subject = LoginValidationsObject.create();
  assert.ok(subject);
});
