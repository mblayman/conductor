import Ember from 'ember';

export default Ember.Route.extend({
  queryParams: {
    search: {
      refreshModel: true
    }
  },

  model(params) {
    if (params.search.length === 0) { return null; }
    return this.store.query('school', params);
  },

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.set('search', '');
    }
  }
});
