import DS from 'ember-data';

import SupportTicketValidations from 'client/mixins/support-ticket-validations';

export default DS.Model.extend(SupportTicketValidations, {
  email: DS.attr('string'),
  subject: DS.attr('string'),
  message: DS.attr('string')
});
