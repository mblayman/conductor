import { mockFindAll, mockSetup, mockTeardown } from 'ember-data-factory-guy';
import { test } from 'qunit';
import moduleForAcceptance from 'client/tests/helpers/module-for-acceptance';

moduleForAcceptance('Acceptance | schools', {
  beforeEach() {
    mockSetup();
  },

  afterEach() {
    mockTeardown();
  }
});

test('visiting /schools', function(assert) {
  mockFindAll('school', 2);

  visit('/schools');

  andThen(function() {
    assert.equal(currentURL(), '/schools');
  });
});
