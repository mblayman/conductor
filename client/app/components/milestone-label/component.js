import { computed } from '@ember/object';
import Component from '@ember/component';

const COLORS = {
  ED: 'pink',
  ED1: 'blue',
  ED2: 'green',
  EA: 'orange',
  RD: 'grey'
};

export default Component.extend({
  tagName: 'span',
  color: computed('milestone.category', function () {
    const category = this.get('milestone.category');
    // When the milestone hasn't resolve yet, return no color.
    if (!category) { return ''; }
    return COLORS[this.get('milestone.category')];
  })
});
