import { moduleForModel, test } from 'ember-qunit';

moduleForModel('target-school', 'Unit | Model | target school', {
  // Specify the other units that are required for this test.
  needs: [
    'model:school',
    'model:student',
  ]
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});

test('has a school', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('school'));
});

test('has a student', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('student'));
});

