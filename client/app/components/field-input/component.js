import Ember from 'ember';
const { computed } = Ember;

export default Ember.Component.extend({
  classNames: ['field'],
  classNameBindings: ['showError:error'],
  hadFocus: false,
  formValidated: false,
  isInvalid: false,
  showError: computed('hadFocus', 'formValidated', 'isInvalid', function() {
    // Show the error message when a user has visited a field
    // or they submit the form and errors exist.
    return (this.get('hadFocus') || this.get('formValidated')) && this.get('isInvalid');
  })
});
