import { moduleForModel, test } from 'ember-qunit';

moduleForModel('invite-email', 'Unit | Model | invite email', {
  // Specify the other units that are required for this test.
  needs: ['validator:format', 'validator:presence']
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});

test('has an email', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('email'));
});
