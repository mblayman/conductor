import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service(),

  actions: {
    authenticate() {
      const credentials = {
        identification: this.get('model').get('username'),
        password: this.get('model').get('password')
      };
      this.get('session').authenticate('authenticator:jwt', credentials).catch((reason) => {
        // TODO: Do something with api errors.
        this.set('errorMessage', reason.error || reason);
      });
    }
  }
});
