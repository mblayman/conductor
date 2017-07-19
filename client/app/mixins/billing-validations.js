import { validator, buildValidations } from 'ember-cp-validations';

export default buildValidations({
  cardNumber: [
    validator('presence', true),
    validator('credit-card-number')
  ],
  cvc: [
    validator('presence', true),
    validator('credit-card-cvc')
  ]
});
