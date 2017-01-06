import Ember from 'ember';

export default Ember.Route.extend({
  // TODO: test this model hook.
  model(params) {
    return this.store.findRecord('student', params.student_id);
  },

  actions: {
    createTargetSchool(school) {
      const student = this.controller.get('model');
      // TODO: Save a target school.
      // TODO: Show error modal if saving fails (e.g., unique constraint failure)
      console.log('From route, creating target school with', school.get('name'), student.get('firstName'));
    }
  }
});
