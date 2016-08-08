import Ember from 'ember';

export default Ember.Route.extend({
  renderTemplate() {
    this.render();
    this.render('index-masthead', {
      into: 'application',
      outlet: 'postHeader'
    });
  }
});
