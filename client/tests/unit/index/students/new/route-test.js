import { run } from '@ember/runloop';
import { manualSetup, mockFindAll } from 'ember-data-factory-guy';
import { moduleFor, test } from 'ember-qunit';

moduleFor('route:index/students/new', 'Unit | Route | index/students/new', {
  beforeEach() {
    manualSetup(this.container);
  },

  needs: [
    'model:school',
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
  let done = assert.async();
  mockFindAll('semester', 2);

  let route = this.subject();
  run(function() {
    let promise = route.model();
    promise.then(function(model) {
      assert.equal(model.student.get('constructor.modelName'), 'student');
      done();
    });
  });
});
