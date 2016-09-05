import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    return this.store.createRecord('invite-email');
  },

  actions: {
    willTransition() {
      // Clean out any unsaved emails from the store.
      const model = this.modelFor(this.routeName);
      model.rollbackAttributes();
    }
  },

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.set('didValidate', false);
      controller.set('errorMessage', false);
    }
  },

  renderTemplate() {
    this.render();
    this.render('index-masthead', {
      into: 'application',
      outlet: 'postHeader'
    });
  }
});
