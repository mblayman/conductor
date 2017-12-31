import Service, { inject as service } from '@ember/service';
import { isEmpty } from '@ember/utils';
import RSVP from 'rsvp';
import JWT from 'ember-simple-auth-token/authenticators/jwt';

export default Service.extend({
  session: service(),
  store: service(),

  load() {
    const token = this.get('session.data.authenticated.token');
    if (!isEmpty(token)) {
      const userId = this.getUserIdFromToken(token);
      return this.get('store').find('user', userId).then((user) => {
        this.set('user', user);
      });
    } else {
      return RSVP.resolve();
    }
  },

  getUserIdFromToken(token) {
    const jwt = new JWT();
    const tokenData = jwt.getTokenData(token);
    return tokenData['user_id'];
  }
});
