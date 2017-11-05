import Ember from 'ember';

export default Ember.Route.extend({
  titleToken(model) {
    return model.get('fullName');
  }
});
