import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('login');
  if (ENABLE_SIGNUP) { // eslint-disable-line no-undef
    this.route('signup');
  }
  this.route('contact');
  // Everything under index is a protected route.
  this.route('index', { path: '/' }, function() {
    this.route('students', function() {
      this.route('new');
    });
    this.route('student', {path: 'students/:student_id'}, function() {
      this.route('find-school');
    });
  });
});

export default Router;
