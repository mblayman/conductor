import signup from './signup';
import studentProfile from './student_profile';

var dispatch = {
  'signup': signup,
  'studentProfile': studentProfile
};

function start(entry, data) {
  dispatch[entry](data);
}

window.start = start;
