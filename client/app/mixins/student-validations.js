import { validator, buildValidations } from 'ember-cp-validations';

export default buildValidations({
  firstName: validator('presence', true),
  lastName: validator('presence', true),
  classYear: [
    validator('presence', true),
    validator('number', {
      integer: true,
      positive: true
    })
  ]
});
