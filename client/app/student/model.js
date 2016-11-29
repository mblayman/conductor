import Model from 'ember-data/model';
import attr from 'ember-data/attr';

import StudentValidations from 'client/mixins/student-validations';

export default Model.extend(StudentValidations, {
  firstName: attr('string'),
  lastName: attr('string'),
});
