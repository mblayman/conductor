import dashboard from './dashboard';
import signup from './signup';
import studentProfile from './student_profile';

var dispatch = {
  'dashboard': dashboard,
  'signup': signup,
  'studentProfile': studentProfile
};

function start(entry, data) {
  dispatch[entry](data);
}

window.start = start;
