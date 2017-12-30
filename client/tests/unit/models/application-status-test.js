import { moduleForModel, test } from 'ember-qunit';

moduleForModel('application-status', 'Unit | Model | application status', {
  // Specify the other units that are required for this test.
  needs: [
    'model:student'
  ]
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});

test('has a student', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('student'));
});

