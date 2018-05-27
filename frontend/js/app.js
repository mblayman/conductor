import signup from './signup';

var dispatch = {
  'signup': signup
};

function start(entry, data) {
  dispatch[entry](data);
}

window.start = start;
