import Route from '@ember/routing/route';

export default Route.extend({
  titleToken: 'Contact',

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
