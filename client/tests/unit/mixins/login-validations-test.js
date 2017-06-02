import Ember from 'ember';
import LoginValidationsMixin from 'client/mixins/login-validations';
import { module, test } from 'qunit';

module('Unit | Mixin | login validations');

// Replace this with your real tests.
test('it works', function(assert) {
  let LoginValidationsObject = Ember.Object.extend(LoginValidationsMixin);
  let subject = LoginValidationsObject.create();
  assert.ok(subject);
});
