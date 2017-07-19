import DS from 'ember-data';

import BillingValidations from 'client/mixins/billing-validations';

export default DS.Model.extend(BillingValidations, {
  cardNumber: DS.attr('string'),
  cvc: DS.attr('number'),
  month: DS.attr('number'),
  year: DS.attr('number')
});
