import { sort } from '@ember/object/computed';
import Controller from '@ember/controller';

export default Controller.extend({
  sortProps: ['name'],
  schools: sort('model.schools.[]', 'sortProps')
});
