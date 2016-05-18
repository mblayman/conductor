import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    submit() {
      console.log(this.get('model').get('email'));
      console.log(this.get('model').get('subject'));
      console.log(this.get('model').get('message'));
      this.get('model').save();
    }
  }
});
