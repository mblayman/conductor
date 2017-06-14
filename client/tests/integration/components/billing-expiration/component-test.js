import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('billing-expiration', 'Integration | Component | billing expiration', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{billing-expiration}}`);

  let rendered = this.$().text().trim();
  assert.notEqual(rendered.indexOf('Expiration'), -1);

  // Template block usage:
  this.render(hbs`
    {{#billing-expiration}}
      template block text
    {{/billing-expiration}}
  `);

  rendered = this.$().text().trim();
  assert.notEqual(rendered.indexOf('template block text'), -1);
});
