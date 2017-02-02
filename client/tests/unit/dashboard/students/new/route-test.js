// import Ember from 'ember';
// import { mockFindAll, mockSetup, mockTeardown } from 'ember-data-factory-guy';
import { moduleFor, test } from 'ember-qunit';

moduleFor('route:dashboard/students/new', 'Unit | Route | dashboard/students/new', {
  // beforeEach() {
  //   mockSetup();
  // },

  // afterEach() {
  //   mockTeardown();
  // },

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

// FIXME: This broke on upgrade to Ember 2.11. No idea why. I reported it.
// https://github.com/danielspaniel/ember-data-factory-guy/issues/273
// test('it has a student for its model', function(assert) {
//   mockFindAll('semester', 2);

//   let route = this.subject();
//   Ember.run(function() {
//     let promise = route.model();
//     promise.then(function(model) {
//       assert.equal(model.student.get('constructor.modelName'), 'student');
//     });
//   });
// });
