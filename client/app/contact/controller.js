import Ember from 'ember';

export default Ember.Controller.extend({
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
    // this.get('model').save();
  }
});
