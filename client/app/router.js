import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('schools');
  this.route('login');
  this.route('signup');
  this.route('terms');
  this.route('contact');
});

export default Router;
