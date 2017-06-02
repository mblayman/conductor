import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('billing-info', 'Integration | Component | billing info', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{billing-info}}`);

  let rendered = this.$().text().trim();
  assert.notEqual(rendered.indexOf('Billing'), -1);

  // Template block usage:
  this.render(hbs`
    {{#billing-info}}
      template block text
    {{/billing-info}}
  `);

  rendered = this.$().text().trim();
  assert.notEqual(rendered.indexOf('template block text'), -1);
});
