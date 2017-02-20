import Model from 'ember-data/model';
import attr from 'ember-data/attr';

export default Model.extend({
  date: attr('date'),
  category: attr('string'),
});
