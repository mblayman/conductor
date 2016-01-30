import TestHelper from 'ember-data-factory-guy/factory-guy-test-helper';
import { test } from 'qunit';
import moduleForAcceptance from 'client/tests/helpers/module-for-acceptance';

moduleForAcceptance('Acceptance | schools', {
  beforeEach() {
    TestHelper.setup();
  },

  afterEach() {
    TestHelper.teardown();
  }
});

test('visiting /schools', function(assert) {
  TestHelper.handleFindAll('school', 2);

  visit('/schools');

  andThen(function() {
    assert.equal(currentURL(), '/schools');
  });
});
