import { moduleForModel, test } from 'ember-qunit';

moduleForModel('support-ticket', 'Unit | Model | support ticket', {
  // Specify the other units that are required for this test.
  needs: []
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

test('has a subject', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('subject'));
});

test('has a message', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('message'));
});
