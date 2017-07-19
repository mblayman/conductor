import { moduleFor, test } from 'ember-qunit';

moduleFor('validator:credit-card-cvc', 'Unit | Validator | credit-card-cvc', {
  needs: [
    'service:stripe',
    'validator:messages'
  ]
});

test('it works', function(assert) {
  var validator = this.subject();
  assert.ok(validator);
});

test('handles a valid CVC', function(assert) {
  var validator = this.subject();
  const isValid = validator.validate('123');
  assert.ok(isValid);
});

test('errors with an invalid CVC', function(assert) {
  var validator = this.subject();
  const errorMessage = validator.validate('');
  assert.notEqual(errorMessage.indexOf('Sorry'), -1);
});
