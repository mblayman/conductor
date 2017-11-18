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

// Quick and dirty method to decode a JWT.
function jwtDecode(rawToken) {
  var token = {};
  token.raw = rawToken;
  token.header = JSON.parse(window.atob(rawToken.split('.')[0]));
  token.payload = JSON.parse(window.atob(rawToken.split('.')[1]));
  return token;
}

/**
 * Transition from landing page to app.
 *
 * Grab a JWT with the new user's credentials,
 * store it in the format that Ember Simple Auth expects,
 * and redirect to the app.
 */
var gotoApp = function(username, password) {
  $.ajax({
    url: window.apiHost + '/api-token-auth/',
    type: 'POST',
    data: {username: username, password: password},
    dateType: 'json'
  })
    .done(function(data) {
      token = jwtDecode(data.token);
      // Store the format that Ember Simple Auth expects to receive.
      var simpleAuthData = {
        authenticated: {
          authenticator: 'authenticator:jwt',
          token: token.raw,
          exp: token.payload.exp
        }
      }
      window.localStorage.setItem(
        'ember_simple_auth-session', JSON.stringify(simpleAuthData));
      window.location.href = '/app';
    })
    .fail(function() {
      var serverError = document.getElementById('server-errors');
      serverError.innerHTML = 'Sorry, we were unable to log you in automatically. ' +
        'We’re redirecting you soon&hellip;';
      setTimeout(function() {
        window.location.href = '/app/login';
      }, 3000);
    });
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
  $.post(window.apiHost + '/users', data)
    .done(function() {
      var username = $form.find('input[name="username"]').val();
      var password = $form.find('input[name="password"]').val();
      gotoApp(username, password);
    })
    .fail(function(jqXHR) {
      var serverError = document.getElementById('server-errors');
      if (jqXHR.responseJSON && jqXHR.responseJSON.errors.length > 0) {
        serverError.textContent = jqXHR.responseJSON.errors[0].detail;
      } else {
        serverError.textContent = 'Sorry, there was a problem handling your request.';
      }
      haltProcessing();
    });
};

// Prevent double clicks with a bit of submit button state management.
var submitState = {
  processing: false,
  buttonText: null,
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


window.addEventListener('load', function() {
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
}, false);
