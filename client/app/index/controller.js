import Ember from 'ember';

export default Ember.Controller.extend({
  flashMessages: Ember.inject.service(),
  successful: false,

  actions: {
    submit() {
      this.get('model').validate().then(({model, validations}) => {
        if (validations.get('isValid')) {
          this.onValid(model);
        } else {
          this.get('flashMessages').warning('Sorry. That doesn’t look like a valid email.');
        }
      });
    }
  },

  onValid(model) {
    model.save()
      .then(this.onSuccess.bind(this))
      .catch(this.onFailure.bind(this));
  },

  onSuccess() {
    this.get('flashMessages').success('Thanks for your interest!', {
      sticky: true
    });
    this.set('successful', true);
  },

  onFailure() {
    this.get('flashMessages').danger('Oops. Something went wrong. Please try again later.');
  }
});
