import TestHelper from 'ember-data-factory-guy/factory-guy-test-helper';
import { test } from 'qunit';
import moduleForAcceptance from 'client/tests/helpers/module-for-acceptance';
import { authenticateSession } from 'client/tests/helpers/ember-simple-auth';

moduleForAcceptance('Acceptance | login', {
  beforeEach() {
    TestHelper.setup();
  },

  afterEach() {
    TestHelper.teardown();
  }
});

test('visiting /login', function(assert) {
  visit('/login');

  andThen(function() {
    assert.equal(currentURL(), '/login');
  });
});

test('visiting /login when already authenticated', function(assert) {
  TestHelper.mockFindAll('student', 2);

  authenticateSession(this.application);
  visit('/login');

  andThen(function() {
    assert.equal(currentURL(), '/dashboard');
  });
});
