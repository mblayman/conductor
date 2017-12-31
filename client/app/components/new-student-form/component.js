import Component from '@ember/component';

export default Component.extend({
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
