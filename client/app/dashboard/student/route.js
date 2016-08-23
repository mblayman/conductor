import Ember from 'ember';

export default Ember.Route.extend({
  // TODO: test this model hook.
  model(params) {
    return this.store.findRecord('student', params.student_id);
  }
});
