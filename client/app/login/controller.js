import Controller from '@ember/controller';

import Authenticator from 'client/mixins/authenticator';

export default Controller.extend(Authenticator, {
  didValidate: false,

  actions: {
    authenticate() {
      this.get('model').validate().then(({model, validations}) => {
        if (validations.get('isValid')) {
          this.authenticate(model.get('username'), model.get('password')).catch(
            (reason) => {
              this.set('errorMessage', reason);
            });
        } else {
          this.set('errorMessage', 'Oops. Something is out of whack.');
        }
        this.set('didValidate', true);
      });
    }
  }
});
