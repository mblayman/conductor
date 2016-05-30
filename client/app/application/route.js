import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {
  title(tokens) {
    tokens.push('College Conductor');
    return tokens.join(' - ');
  }
});
