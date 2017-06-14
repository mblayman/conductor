import Ember from 'ember';
import moment from 'moment';
const { computed } = Ember;

export default Ember.Component.extend({
  didInsertElement() {
    this._super(...arguments);
    this.$('select.dropdown').dropdown();
  },

  years: computed('', () => {
    const maxYears = 15;
    const year = moment().year();
    let years = [];
    for (let i = 0; i < maxYears; i++) {
      years.push(year + i);
    }
    return years;
  })
});
