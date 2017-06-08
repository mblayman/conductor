import Ember from 'ember';

export default Ember.Mixin.create({
  session: Ember.inject.service(),

  authenticate(username, password) {
    const credentials = {
      identification: username,
      password: password
    };
    return this.get('session').authenticate('authenticator:jwt', credentials).catch(
      (reason) => {
        if (reason === undefined) {
          throw 'Hmm. We can’t seem to connect right now.';
        } else {
          throw reason['non_field_errors'][0];
        }
      });
  }
});
