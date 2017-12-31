import EmberObject from '@ember/object';
import StudentValidationsMixin from 'client/mixins/student-validations';
import { module, test } from 'qunit';

module('Unit | Mixin | student validations');

// Replace this with your real tests.
test('it works', function(assert) {
  let StudentValidationsObject = EmberObject.extend(StudentValidationsMixin);
  let subject = StudentValidationsObject.create();
  assert.ok(subject);
});
