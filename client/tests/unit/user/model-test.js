import { moduleForModel, test } from 'ember-qunit';

moduleForModel('user', 'Unit | Model | user', {
  // Specify the other units that are required for this test.
  needs: [
    'validator:presence'
  ]
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});

test('has a username', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('username'));
});

test('has an email', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('email'));
});

test('has a password', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('password'));
});
