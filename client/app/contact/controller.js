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
    console.log(model.get('email'));
    console.log(model.get('subject'));
    console.log(model.get('message'));
    this.get('flashMessages').success('Thanks! We will get back to you soon.');
    // this.get('model').save();
  }
});
