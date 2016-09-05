import Ember from 'ember';
import InviteEmailValidationsMixin from 'client/mixins/invite-email-validations';
import { module, test } from 'qunit';

module('Unit | Mixin | invite email validations');

// Replace this with your real tests.
test('it works', function(assert) {
  let InviteEmailValidationsObject = Ember.Object.extend(InviteEmailValidationsMixin);
  let subject = InviteEmailValidationsObject.create();
  assert.ok(subject);
});
