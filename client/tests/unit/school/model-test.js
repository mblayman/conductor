import { moduleForModel, test } from 'ember-qunit';

moduleForModel('school', 'Unit | Model | school', {
  // Specify the other units that are required for this test.
  needs: [
    'model:milestone',
  ]
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});

test('has a name', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('name'));
});

test('has many milestones', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('milestones'));
});
