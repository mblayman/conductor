import EmberRouter from '@ember/routing/router';
import config from './config/environment';

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('login');
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
