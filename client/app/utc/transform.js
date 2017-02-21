import moment from 'moment';
import DS from 'ember-data';

export default DS.Transform.extend({
  deserialize(serialized) {
    return moment.utc(serialized);
  },

  serialize(deserialized) {
    return deserialized ? deserialized.toJSON() : null;
  }
});
