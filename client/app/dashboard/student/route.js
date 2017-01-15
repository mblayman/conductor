import Ember from 'ember';

export default Ember.Route.extend({
  flashMessages: Ember.inject.service(),

  // TODO: test this model hook.
  model(params) {
    return this.store.findRecord('student', params.student_id, {include: 'schools'});
  },

  actions: {
    createTargetSchool(school) {
      const student = this.controller.get('model');
      const targetSchool = this.store.createRecord(
        'target-school', {school: school, student: student});
      targetSchool.save().then(() => {
        student.reload();
        this.transitionTo('dashboard.student');
      }).catch((reason) => {
        if (reason.errors.length >= 1 && reason.errors[0].detail.includes('unique')) {
          this.get('flashMessages').danger(
            `${school.get('name')} is already one of ${student.get('firstName')}’s schools.`);
        } else {
          this.get('flashMessages').danger(
            'Oops. Something went wrong. Please try again later.');
        }
      });
    }
  }
});
