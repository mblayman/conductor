import { moduleFor, test } from 'ember-qunit';

moduleFor('route:dashboard/student', 'Unit | Route | dashboard/student', {
  // Specify the other units that are required for this test.
  needs: [
    'service:flashMessages'
  ]
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
