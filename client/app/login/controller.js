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
            if (reason === undefined) {
              this.set('errorMessage', 'Hmm. We can’t seem to connect right now.');
            } else {
              this.set('errorMessage', reason['non_field_errors'][0]);
            }
          });
        } else {
          this.set('errorMessage', 'Oops. Something is out of whack.');
        }
        this.set('didValidate', true);
      });
    }
  }
});
