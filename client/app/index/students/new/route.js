import { hash } from 'rsvp';
import Route from '@ember/routing/route';

export default Route.extend({
  titleToken: 'Add a student',

  model() {
    return hash({
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
