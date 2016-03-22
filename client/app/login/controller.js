import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service(),

  actions: {
    authenticate() {
      const credentials = this.getProperties('identification', 'password');
      const authenticator = 'authenticator:jwt';
      this.get('session').authenticate(authenticator, credentials).catch((reason) => {
          this.set('errorMessage', reason.error || reason);
      });
    }
  }
});
