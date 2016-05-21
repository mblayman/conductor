import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    return this.store.createRecord('support-ticket');
  },

  // Controllers are singletons so state must be cleared.
  setupController(controller, model) {
    this._super(controller, model);
    controller.set('didValidate', false);
    controller.set('successful', false);
  }
});
