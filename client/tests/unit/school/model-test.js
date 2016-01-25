import { moduleForModel, test } from 'ember-qunit';

moduleForModel('school', 'Unit | Model | school', {
  // Specify the other units that are required for this test.
  needs: []
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});

test('has a name', function(assert) {
  let model = this.subject();
  let hasName = Object.keys(model.toJSON()).indexOf('name') > -1;
  assert.ok(hasName);
});
