import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement() {
    this._super(...arguments);
    this.$('select.dropdown').dropdown();
  },

  actions: {
    selectSemester(semester) {
      this.get('student').set('matriculationSemester', semester);
    }
  }
});
