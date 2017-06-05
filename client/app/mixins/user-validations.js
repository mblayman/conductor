import { validator, buildValidations } from 'ember-cp-validations';

export default buildValidations({
  username: [
    validator('presence', true),
    validator('unique-username', {debounce: 300})
  ],
  email: [
    validator('presence', true),
    validator('format', {type: 'email'}),
    validator('unique-email', {debounce: 300})
  ],
  password: [
    validator('presence', true),
    validator('length', {min: 10})
  ]
});
