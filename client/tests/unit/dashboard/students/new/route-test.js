import Ember from 'ember';
import { moduleFor, test } from 'ember-qunit';

moduleFor('route:dashboard/students/new', 'Unit | Route | dashboard/students/new', {
  needs: [
    'model:student',
    'validator:number',
    'validator:presence'
  ]
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});

test('it has a student for its model', function(assert) {
  let route = this.subject();
  Ember.run(function() {
    let student = route.model();
    assert.equal(student.get('constructor.modelName'), 'student');
  });
});
