import Ember from 'ember';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';
import LoginValidationsMixin from 'client/mixins/login-validations';

const Login = Ember.Object.extend(LoginValidationsMixin, {
  username: null,
  password: null
});

export default Ember.Route.extend(UnauthenticatedRouteMixin, {
  titleToken: 'Login',

  model() {
    return Login.create(Ember.getOwner(this).ownerInjection());
  },

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.set('didValidate', false);
      controller.set('errorMessage', false);
    }
  }
});
