import DS from 'ember-data';

export default DS.Model.extend({
  cardNumber: DS.attr('string'),
  cvc: DS.attr('number'),
  month: DS.attr('number'),
  year: DS.attr('number')
});
