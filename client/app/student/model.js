import Ember from 'ember';
import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';

import StudentValidations from 'client/mixins/student-validations';

const { computed } = Ember;

export default Model.extend(StudentValidations, {
  firstName: attr('string'),
  lastName: attr('string'),
  matriculationSemester: belongsTo('semester'),
  schools: hasMany('school'),

  fullName: computed('firstName', 'lastName', function() {
    return `${this.get('firstName')} ${this.get('lastName')}`;
  })
});
