import { moduleFor, test } from 'ember-qunit';

moduleFor('validator:unique-email', 'Unit | Validator | unique-email', {
  needs: ['validator:messages']
});

test('it works', function(assert) {
  var validator = this.subject();
  assert.ok(validator);
});
