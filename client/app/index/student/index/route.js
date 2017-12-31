import Route from '@ember/routing/route';

export default Route.extend({
  titleToken(model) {
    return model.get('fullName');
  },

  actions: {
    triggerExport(student) {
      const applicationStatus = this.store.createRecord('application-status', { student });
      applicationStatus.save();
    }
  }
});
