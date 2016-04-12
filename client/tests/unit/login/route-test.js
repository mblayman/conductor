import Ember from 'ember';
import { moduleFor, test } from 'ember-qunit';

moduleFor('route:login', 'Unit | Route | login', {
  needs: ['model:user']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});

test('has a user for its model', function(assert) {
  let route = this.subject();
  Ember.run(function() {
    let user = route.model();
    assert.equal(user.get('constructor.modelName'), 'user');
  });
});
