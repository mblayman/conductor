import Ember from 'ember';
import AuthenticatorMixin from 'client/mixins/authenticator';
import { module, test } from 'qunit';

module('Unit | Mixin | authenticator');

// Replace this with your real tests.
test('it works', function(assert) {
  let AuthenticatorObject = Ember.Object.extend(AuthenticatorMixin);
  let subject = AuthenticatorObject.create();
  assert.ok(subject);
});
