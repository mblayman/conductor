import DS from 'ember-data';

export default DS.Model.extend({
  school: DS.belongsTo('school'),
  student: DS.belongsTo('student')
});
