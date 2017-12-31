import EmberObject from '@ember/object';
import SupportTicketValidationsMixin from 'client/mixins/support-ticket-validations';
import { module, test } from 'qunit';

module('Unit | Mixin | support ticket validations');

// Replace this with your real tests.
test('it works', function(assert) {
  let SupportTicketValidationsObject = EmberObject.extend(SupportTicketValidationsMixin);
  let subject = SupportTicketValidationsObject.create();
  assert.ok(subject);
});
