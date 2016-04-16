import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service(),
  didValidate: false,

  actions: {
    authenticate() {
      this.get('model').validate().then(({model, validations}) => {
        if (validations.get('isValid')) {
          const credentials = {
            identification: model.get('username'),
            password: model.get('password')
          };
          this.get('session').authenticate('authenticator:jwt', credentials).catch((reason) => {
            // TODO: Do something with api errors.
            this.set('errorMessage', reason.error || reason);
          });
        } else {
          // TODO: This will probably break if more validations are added to user.
          // Clear any previous submission to the server.
          this.set('errorMessage', '');
        }
        this.set('didValidate', true);
      });
    }
  }
});
