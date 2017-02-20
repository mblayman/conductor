import { moduleForModel, test } from 'ember-qunit';

moduleForModel('milestone', 'Unit | Model | milestone', {
  // Specify the other units that are required for this test.
  needs: []
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});

test('has a date', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('date'));
});

test('has a category', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('category'));
});
