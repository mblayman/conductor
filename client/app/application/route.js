import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Route.extend(ApplicationRouteMixin, {
  currentUser: service(),
  segment: service(),

  routeAfterAuthentication: 'index',
  routeIfAlreadyAuthenticated: 'index',

  beforeModel() {
    return this._loadCurrentUser();
  },

  sessionAuthenticated() {
    this._super(...arguments);
    this._loadCurrentUser().catch(() => this.get('session').invalidate());
  },

  _loadCurrentUser() {
    return this.get('currentUser').load();
  },

  title(tokens) {
    tokens.reverse();
    tokens.push('College Conductor');
    return tokens.join(' - ');
  },

  identifyUser() {
    const user = this.get('currentUser.user');
    if (user) {
      this.get('segment').identifyUser(user.get('id'), {username: user.get('username')});
    }
  }
});
