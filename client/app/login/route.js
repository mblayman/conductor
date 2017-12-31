import { getOwner } from '@ember/application';
import Route from '@ember/routing/route';
import EmberObject from '@ember/object';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';
import LoginValidationsMixin from 'client/mixins/login-validations';

const Login = EmberObject.extend(LoginValidationsMixin, {
  username: null,
  password: null
});

export default Route.extend(UnauthenticatedRouteMixin, {
  titleToken: 'Login',

  model() {
    return Login.create(getOwner(this).ownerInjection());
  },

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.set('didValidate', false);
      controller.set('errorMessage', false);
    }
  }
});
