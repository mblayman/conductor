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

  actions: {
    loading(transition) {
      let controller = this.controllerFor('dashboard.student.find-school');
      controller.set('currentlyLoading', true);
      transition.promise.finally(function() {
          controller.set('currentlyLoading', false);
      });
    }
  },

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.set('currentlyLoading', false);
      controller.set('search', '');
    }
  }
});
