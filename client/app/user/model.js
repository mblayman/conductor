import DS from 'ember-data';

import UserValidations from 'client/mixins/user-validations';

export default DS.Model.extend(UserValidations, {
  username: DS.attr('string'),
  email: DS.attr('string'),
});
