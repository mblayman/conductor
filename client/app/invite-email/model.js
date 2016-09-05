import DS from 'ember-data';

import InviteEmailValidations from 'client/mixins/invite-email-validations';

export default DS.Model.extend(InviteEmailValidations, {
  email: DS.attr('string')
});
