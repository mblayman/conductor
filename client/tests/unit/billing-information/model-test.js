import { moduleForModel, test } from 'ember-qunit';

moduleForModel('billing-information', 'Unit | Model | billing information', {
  // Specify the other units that are required for this test.
  needs: [
    'validator:presence',
    'validator:credit-card-number',
    'validator:credit-card-cvc'
  ]
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});

test('has a card number', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('cardNumber'));
});

test('has a CVC', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('cvc'));
});

test('has a month', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('month'));
});

test('has a year', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('year'));
});
