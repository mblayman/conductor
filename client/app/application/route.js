import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

const { service } = Ember.inject;

export default Ember.Route.extend(ApplicationRouteMixin, {
  currentUser: service(),
  segment: service(),

  routeAfterAuthentication: 'dashboard',
  routeIfAlreadyAuthenticated: 'dashboard',

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
