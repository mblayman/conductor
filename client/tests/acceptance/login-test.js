import { test } from 'qunit';
import moduleForAcceptance from 'client/tests/helpers/module-for-acceptance';
import { authenticateSession } from 'client/tests/helpers/ember-simple-auth';

moduleForAcceptance('Acceptance | login');

test('visiting /login', function(assert) {
  visit('/login');

  andThen(function() {
    assert.equal(currentURL(), '/login');
  });
});

test('visiting /login when already authenticated', function(assert) {
  authenticateSession(this.application);
  visit('/login');

  andThen(function() {
    assert.equal(currentURL(), '/');
  });
});
