import EmberObject, { computed } from '@ember/object';
import Controller from '@ember/controller';

export default Controller.extend({
  queryParams: {
    search: 'q'
  },
  search: '',
  currentlyLoading: false,
  schoolOptions: computed('model.@each', function() {
    let schools = this.get('student.schools');
    return this.get('model').map((school) => {
      return EmberObject.create({
        school: school,
        isTargetSchool: schools.includes(school)
      });
    });
  })
});
