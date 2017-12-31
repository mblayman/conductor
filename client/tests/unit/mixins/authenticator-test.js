import EmberObject from '@ember/object';
import AuthenticatorMixin from 'client/mixins/authenticator';
import { module, test } from 'qunit';

module('Unit | Mixin | authenticator');

// Replace this with your real tests.
test('it works', function(assert) {
  let AuthenticatorObject = EmberObject.extend(AuthenticatorMixin);
  let subject = AuthenticatorObject.create();
  assert.ok(subject);
});
