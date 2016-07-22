import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['field'],
  classNameBindings: ['isInvalid:error']
});
