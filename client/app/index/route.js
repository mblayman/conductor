import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    return this.store.createRecord('invite-email');
  },

  renderTemplate() {
    this.render();
    this.render('index-masthead', {
      into: 'application',
      outlet: 'postHeader'
    });
  }
});
