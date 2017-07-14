import { moduleFor, test } from 'ember-qunit';

moduleFor('validator:credit-card-number', 'Unit | Validator | credit-card-number', {
  needs: [
    'service:stripe',
    'validator:messages'
  ]
});

test('it works', function(assert) {
  var validator = this.subject();
  assert.ok(validator);
});

test('handles a valid card number', function(assert) {
  var validator = this.subject();
  const isValid = validator.validate('4242 4242 4242 4242');
  assert.ok(isValid);
});

test('errors with an invalid card', function(assert) {
  var validator = this.subject();
  const errorMessage = validator.validate('bogus card');
  assert.notEqual(errorMessage.indexOf('Sorry'), -1);
});
