import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('new-student-form', 'Integration | Component | new student form', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });
  this.set('noop', () => {});

  this.render(hbs`{{new-student-form onSubmit=(action noop)}}`);

  let rendered = this.$().text().trim();
  assert.notEqual(rendered.indexOf('Add a student'), -1);

  // Template block usage:
  this.render(hbs`
    {{#new-student-form onSubmit=(action noop)}}
      template block text
    {{/new-student-form}}
  `);

  rendered = this.$().text().trim();
  assert.notEqual(rendered.indexOf('template block text'), -1);
});
