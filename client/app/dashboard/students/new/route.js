import Ember from 'ember';

export default Ember.Route.extend({
  titleToken: 'Add a student',

  model() {
    return this.store.createRecord('student');
  },

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.set('didValidate', false);
      controller.set('errorMessage', false);
    }
  }
});
