import Ember from 'ember';
import BaseValidator from 'ember-cp-validations/validators/base';

const UniqueUsername = BaseValidator.extend({
  store: Ember.inject.service(),

  validate(value) {
    return this.get('store').query('user', {
      filter: {username: value}
    })
      .then((result) => {
        if (result.get('length') === 0) {
          return true;
        } else {
          return 'Sorry, that username is unavailable.'
        }
      });
  }
});

UniqueUsername.reopenClass({
  /**
   * Define attribute specific dependent keys for your validator
   *
   * [
   * 	`model.array.@each.${attribute}` --> Dependent is created on the model's context
   * 	`${attribute}.isValid` --> Dependent is created on the `model.validations.attrs` context
   * ]
   *
   * @param {String}  attribute   The attribute being evaluated
   * @param {Unknown} options     Options passed into your validator
   * @return {Array}
   */
  getDependentsFor(/* attribute, options */) {
    return [];
  }
});

export default UniqueUsername;
