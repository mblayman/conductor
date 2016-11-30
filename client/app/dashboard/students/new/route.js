import Ember from 'ember';

export default Ember.Route.extend({
  titleToken: 'Add a student',

  model() {
    return Ember.RSVP.hash({
      student: this.store.createRecord('student'),
      semesters: this.store.findAll('semester')
    });
  },

  actions: {
    willTransition() {
      // Clean out any unsaved students from the store.
      const model = this.modelFor(this.routeName);
      model.student.rollbackAttributes();
    }
  },

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.set('didValidate', false);
      controller.set('errorMessage', false);
    }
  }
});
