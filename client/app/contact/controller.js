import Ember from 'ember';

export default Ember.Controller.extend({
  flashMessages: Ember.inject.service(),
  didValidate: false,

  actions: {
    submit() {
      this.get('model').validate().then(({model, validations}) => {
        if (validations.get('isValid')) {
          this.onValid(model);
        }
        this.set('didValidate', true);
      });
    }
  },

  onValid(model) {
    model.save()
      .then(this.onSuccess.bind(this))
      .catch(this.onFailure.bind(this));
  },

  onSuccess() {
    this.get('flashMessages').success('Thanks! We will get back to you soon.');
  },

  onFailure() {
    this.get('flashMessages').danger('Oops. Something went wrong. Please try again later.');
  }
});
