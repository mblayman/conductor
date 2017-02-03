import Ember from 'ember';

export default Ember.Controller.extend({
  sortProps: ['name'],
  schools: Ember.computed.sort('model.schools.[]', 'sortProps')
});
