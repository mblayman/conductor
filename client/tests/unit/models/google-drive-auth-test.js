import { moduleForModel, test } from 'ember-qunit';

moduleForModel('google-drive-auth', 'Unit | Model | google drive auth', {
  // Specify the other units that are required for this test.
  needs: []
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});

test('has a code', function(assert) {
  let model = this.subject();
  assert.ok(model.toJSON().hasOwnProperty('code'));
});
