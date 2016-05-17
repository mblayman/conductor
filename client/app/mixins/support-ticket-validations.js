import { validator, buildValidations } from 'ember-cp-validations';

export default buildValidations({
  email: [
    validator('presence', true),
    validator('format', {type: 'email'})
  ],
  subject: validator('presence', true),
  message: validator('presence', true)
});
