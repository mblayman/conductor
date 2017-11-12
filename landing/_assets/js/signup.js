// Create a Stripe client.
var stripe = Stripe(window.stripePublishableKey);

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#868e96'
    }
  },
  invalid: {
    color: '#dc3545',
    iconColor: '#dc3545'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

$('#why-ask').popover({
  trigger: 'focus'
});

var completeSignup = function(stripeToken) {
  // Check the validity again in case creating a token took a long time
  // and the user somehow managed to screw up the form.
  var form = document.getElementById('signup-form');
  if (!form.checkValidity()) { return; }
  var $form = $(form);
  var data = $form.serializeArray();
  data.push({name: 'stripe_token', value: stripeToken.id});
  data.push({name: 'postal_code', value: stripeToken.card.address_zip});
  // TODO: Send data to API.
  $.post('https://localhost:8080/users', data)
    .done(function() {
      // TODO: redirect to app (and authenticate?)
      console.log('it worked');
    })
    .fail(function(jqXHR, textStatus, error) {
      var serverError = document.getElementById('server-errors');
      if (jqXHR.responseJSON && jqXHR.responseJSON.errors.length > 0) {
        serverError.textContent = jqXHR.responseJSON.errors[0].detail;
      } else {
        serverError.textContent = 'Sorry, there was a problem handling your request.';
      }
    });
};

window.addEventListener('load', function() {
  var form = document.getElementById('signup-form');
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    event.stopPropagation();

    // Check the regular form fields.
    var isValid = form.checkValidity();

    stripe.createToken(card).then(function(result) {
      if (result.error) {
        var errorElement = document.getElementById('card-errors');
        errorElement.textContent = result.error.message;
      } else {
        completeSignup(result.token);
      }
    });

    form.classList.add('was-validated');
  }, false);
}, false);
