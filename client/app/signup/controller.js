import Ember from 'ember';

import Authenticator from 'client/mixins/authenticator';

export default Ember.Controller.extend(Authenticator, {
  didValidate: false,

  actions: {
    signUp() {
      this.get('model').validate().then(({model, validations}) => {
        if (validations.get('isValid')) {
          model.save().then(() => {
            this.authenticate(model.get('username'), model.get('password')).catch(
              (reason) => {
                this.set('errorMessage', reason);
              });
          });
        } else {
          this.set('errorMessage', 'Oops. Something is out of whack.');
        }
        this.set('didValidate', true);
      });
    }
  }
});
