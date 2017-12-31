import { inject as service } from '@ember/service';
import Mixin from '@ember/object/mixin';

export default Mixin.create({
  session: service(),

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
