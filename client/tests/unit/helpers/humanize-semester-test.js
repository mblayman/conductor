import { make, manualSetup } from 'ember-data-factory-guy';
import { humanizeSemester } from 'client/helpers/humanize-semester';
import { moduleForModel, test } from 'ember-qunit';

moduleForModel('semester', 'Unit | Helper | humanize semester', {
  beforeEach() {
    manualSetup(this.container);
  }
});

test('it matches a fall semester', function(assert) {
  let semester = make('semester', {date: new Date('2018-11-15')});
  let result = humanizeSemester([semester]);
  assert.equal(result, 'Fall 2018');
});

test('it matches a spring semester', function(assert) {
  let semester = make('semester', {date: new Date('2019-04-15')});
  let result = humanizeSemester([semester]);
  assert.equal(result, 'Spring 2019');
});

test('it matches a summer semester', function(assert) {
  let semester = make('semester', {date: new Date('2019-07-15')});
  let result = humanizeSemester([semester]);
  assert.equal(result, 'Summer 2019');
});
