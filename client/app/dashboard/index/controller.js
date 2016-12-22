import Ember from 'ember';

export default Ember.Controller.extend({
  studentsBySemester: Ember.computed.sort('model', (a, b) => {
    // XXX: This only works after the semesters resolve. Because side
    // loading is not working, these aren't resolved on first render.
    // There's probably a way to force recalculation when the semesters
    // resolve, but I don't know how right now.
    if (a.get('matriculationSemester.date') < b.get('matriculationSemester.date')) {
      return -1;
    } else if (a.get('matriculationSemester.date') > b.get('matriculationSemester.date')) {
      return 1;
    }
    return 0;
  })
});
