import { validator, buildValidations } from 'ember-cp-validations';

export default buildValidations({
  username: validator('presence', true),
  password: validator('presence', true)
});
