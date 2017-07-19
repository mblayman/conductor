import BaseValidator from 'ember-cp-validations/validators/base';
import Ember from 'ember';

const CreditCardCvc = BaseValidator.extend({
  stripe: Ember.inject.service(),

  validate(value) {
    const isValid = this.get('stripe').card.validateCVC(value);
    if (isValid) {
      return true;
    }
    return 'Sorry, the card CVC is not valid.';
  }
});

CreditCardCvc.reopenClass({
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

export default CreditCardCvc;
