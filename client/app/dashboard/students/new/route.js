import Ember from 'ember';

export default Ember.Route.extend({
  titleToken: 'Add a student',

  model() {
    return this.store.createRecord('student');
  },

  actions: {
    willTransition() {
      // Clean out any unsaved students from the store.
      const model = this.modelFor(this.routeName);
      model.rollbackAttributes();
    }
  },

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.set('didValidate', false);
      controller.set('errorMessage', false);
    }
  }
});
