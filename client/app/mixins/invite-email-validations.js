import { validator, buildValidations } from 'ember-cp-validations';

export default buildValidations({
  email: [
    validator('presence', true),
    validator('format', {type: 'email'})
  ]
});
