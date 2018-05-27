import $ from 'jquery';
import 'bootstrap';

// Prevent double clicks with a bit of submit button state management.
var submitState = {
  processing: false,
  buttonText: null,
};

var completeSignup = function(stripeToken) {
  // Check the validity again in case creating a token took a long time
  // and the user somehow managed to screw up the form.
  var form = document.getElementById('signup-form');
  if (!form.checkValidity()) {
    haltProcessing();
    return;
  }
  var $form = $(form);
  var data = $form.serializeArray();
  data.push({name: 'stripe_token', value: stripeToken.id});
  data.push({name: 'postal_code', value: stripeToken.card.address_zip});
  $.post($form.attr('action'), data)
    .done(function(data) {
      if (data.status === 'success') {
        window.location.href = '/app/';
      } else {
        // Keep track of the error keys so errors can be cleared
        // with resubmissions.
        var errorKeys = ['username', 'email', 'password', '__all__'];
        for (var i = 0; i < errorKeys.length; i++) {
          var errorKey = errorKeys[i];
          var errorText = '';
          if (data.errors.hasOwnProperty(errorKey)) {
            for (var j = 0; j < data.errors[errorKey].length; j++) {
              errorText += data.errors[errorKey][j] + ' ';
            }
          }
          var errorElement = document.getElementById(errorKey + '-errors');
          errorElement.textContent = errorText;
        }
        haltProcessing();
      }
    })
    .fail(function(jqXHR) {
      var serverError = document.getElementById('__all__-errors');
      serverError.textContent = 'Sorry, there was a problem handling your request.';
      haltProcessing();
    });
};

/**
 * Check if the form is processing and lock if it's not.
 */
var isProcessing = function() {
  if (submitState.processing) { return true; }
  submitState.processing = true;
  var $submit = $('#signup-form').find(':submit')
  $submit.prop('disabled', true);
  submitState.buttonText = $submit.html();
  $submit.html('<i class="fa fa-circle-o-notch fa-spin fa-lg"></i>');
  return false;
}

/**
 * Halt processing and clean up the button.
 */
var haltProcessing = function() {
  var $submit = $('#signup-form').find(':submit')
  $submit.prop('disabled', false);
  $submit.html(submitState.buttonText);
  submitState.processing = false;
}

export default function(data) {
  // Create a Stripe client.
  var stripe = Stripe(data.stripePublishableKey);

  // Create an instance of Elements.
  var elements = stripe.elements();

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

  var form = document.getElementById('signup-form');
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    event.stopPropagation();
    if (isProcessing()) { return; }

    // Check the regular form fields.
    var isValid = form.checkValidity();

    stripe.createToken(card).then(function(result) {
      if (result.error) {
        var errorElement = document.getElementById('card-errors');
        errorElement.textContent = result.error.message;
        haltProcessing();
      } else {
        completeSignup(result.token);
      }
    });

    form.classList.add('was-validated');
    if (!isValid) {
      haltProcessing();
    }
  }, false);
}
