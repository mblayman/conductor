import Ember from 'ember';
import BillingValidationsMixin from 'client/mixins/billing-validations';
import { module, test } from 'qunit';

module('Unit | Mixin | billing validations');

// Replace this with your real tests.
test('it works', function(assert) {
  let BillingValidationsObject = Ember.Object.extend(BillingValidationsMixin);
  let subject = BillingValidationsObject.create();
  assert.ok(subject);
});
