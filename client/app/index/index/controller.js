import Ember from 'ember';

export default Ember.Controller.extend({
  sortProps: ['lastName'],
  students: Ember.computed.sort('model', 'sortProps')
});
