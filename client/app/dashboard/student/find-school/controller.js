import Ember from 'ember';

export default Ember.Controller.extend({
  queryParams: {
    search: 'q'
  },
  search: '',
  currentlyLoading: false,
  schoolOptions: Ember.computed('model.@each', function() {
    let schools = this.get('student.schools');
    return this.get('model').map((school) => {
      return Ember.Object.create({
        school: school,
        isTargetSchool: schools.includes(school)
      });
    });
  })
});
