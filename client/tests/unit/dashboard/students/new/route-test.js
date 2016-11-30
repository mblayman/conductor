import Ember from 'ember';
import TestHelper from 'ember-data-factory-guy/factory-guy-test-helper';
import { moduleFor, test } from 'ember-qunit';

moduleFor('route:dashboard/students/new', 'Unit | Route | dashboard/students/new', {
  beforeEach() {
    TestHelper.setup();
  },

  afterEach() {
    TestHelper.teardown();
  },

  needs: [
    'model:semester',
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
  TestHelper.mockFindAll('semester', 2);

  let route = this.subject();
  Ember.run(function() {
    let promise = route.model();
    promise.then(function(model) {
      assert.equal(model.student.get('constructor.modelName'), 'student');
    });
  });
});
