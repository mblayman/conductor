import Ember from 'ember';
import { moduleFor, test } from 'ember-qunit';

moduleFor('route:index', 'Unit | Route | index', {
  // Specify the other units that are required for this test.
  needs: [
    'model:invite-email',
    'validator:format',
    'validator:presence'
  ]
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});

test('it has an invite email for its model', function(assert) {
  let route = this.subject();
  Ember.run(function() {
    let inviteEmail = route.model();
    assert.equal(inviteEmail.get('constructor.modelName'), 'invite-email');
  });
});
