import resolver from './helpers/resolver';
import {
  setResolver
} from 'ember-qunit';

// XXX: This is what I get for being on the bleeding edge. Bugs.
// See emberjs/data#4071.
import "ember-data";

setResolver(resolver);
