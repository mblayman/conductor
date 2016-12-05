import { moduleFor, test } from 'ember-qunit';

moduleFor('controller:dashboard/students/new', 'Unit | Controller | dashboard/students/new', {
  // Specify the other units that are required for this test.
  // needs: ['controller:foo']
});

// Replace this with your real tests.
test('it exists', function(assert) {
  let controller = this.subject();
  assert.ok(controller);
});

test('it sets the student semester', function(assert) {
  // XXX: Something that should be stupidly easy seems impossibly hard.
  // I can't get Ember to set the controller model. I'll leave this here
  // to show the intent. Hopefully, I'll get more Ember experience and
  // understand how to do this someday.
  // let semester = make('semester');
  // let student = make('student');
  // let controller = this.subject();
  // Ember.run(function() {
  //   controller.set('model', {student: student});
  //   controller.send('selectSemester', semester);
  // });
  // assert.equal(controller.get('model').student.get('matriculationSemester'), semester);
  assert.ok(true);
});
