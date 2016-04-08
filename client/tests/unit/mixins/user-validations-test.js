import Ember from 'ember';
import UserValidationsMixin from 'client/mixins/user-validations';
import { module, test } from 'qunit';

module('Unit | Mixin | user validations');

// Replace this with your real tests.
test('it works', function(assert) {
  let UserValidationsObject = Ember.Object.extend(UserValidationsMixin);
  let subject = UserValidationsObject.create();
  assert.ok(subject);
});
