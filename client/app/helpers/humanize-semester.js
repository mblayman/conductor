import Ember from 'ember';

/*
 * Get the season. This is a crude approximation, but it will work.
 */
function getSeason(month) {
  if (month < 6) {
    return 'Spring';
  } else if (month < 9) {
    return 'Summer';
  }
  return 'Fall';
}

export function humanizeSemester(params) {
  let semester = params[0];
  let season = getSeason(semester.get('date').getMonth());
  let year = semester.get('date').getFullYear();
  return `${season} ${year}`;
}

export default Ember.Helper.helper(humanizeSemester);
