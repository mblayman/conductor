import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('schools');
  this.route('login');
  if (ENABLE_SIGNUP) {
    this.route('signup');
  }
  this.route('terms');
  this.route('contact');
  this.route('privacy');
  this.route('dashboard', function() {
    this.route('students', function() {
      this.route('new');
    });
    this.route('student', {path: 'students/:student_id'}, function() {
      this.route('find-school');
    });
  });
});

export default Router;
