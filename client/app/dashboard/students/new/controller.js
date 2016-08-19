import Ember from 'ember';

export default Ember.Controller.extend({
  didValidate: false,

  onSuccess() {
    this.transitionToRoute('dashboard');
  },

  onFailure() {
    this.set(
      'errorMessage',
      'Huh? Something bad happened. Please contact support if it continues.');
  },

  actions: {
    create() {
      this.get('model').validate().then(({model, validations}) => {
        if (validations.get('isValid')) {
          model.save()
            .then(this.onSuccess.bind(this))
            .catch(this.onFailure.bind(this));
        } else {
          // TODO: There needs to be some kind of reset when leaving login.
          // Clear any previous submission to the server.
          this.set('errorMessage', 'Oops. Something is out of whack.');
        }
        this.set('didValidate', true);
      });
    }
  }
});
