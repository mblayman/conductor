import Ember from 'ember';

const COLORS = {
  ED: 'pink',
  ED1: 'blue',
  ED2: 'green',
  EA: 'orange',
  RD: 'grey'
};

export default Ember.Component.extend({
  tagName: 'span',
  color: Ember.computed('milestone.category', function () {
    const category = this.get('milestone.category');
    // When the milestone hasn't resolve yet, return no color.
    if (!category) { return ''; }
    return COLORS[this.get('milestone.category')];
  })
});
