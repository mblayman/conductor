import Ember from 'ember';

export default Ember.Controller.extend({
  queryParams: {
    search: 'q'
  },
  search: '',
  currentlyLoading: false
});
