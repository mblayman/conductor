import $ from 'jquery';
import 'datatables';
import {on} from 'delegated-events';

import utils from './utils';

function checkStatus(response) {
  if (response.ok) {
    return response
  } else {
    var error = new Error(response.statusText)
    error.response = response
    throw error
  }
}

function parseJSON(response) {
  return response.json()
}

function makeSendMilestone(studentMilestonesUrl) {
  return function(milestoneId) {
    milestoneId = parseInt(milestoneId, 10)
    return fetch(studentMilestonesUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': utils.getCsrfToken()
      },
      body: JSON.stringify({'milestone': milestoneId})
    })
    .then(checkStatus)
    .then(parseJSON)
  }
}

let lockedMilestones = [];

function isMilestoneLocked(milestoneId) {
  return lockedMilestones.includes(milestoneId);
}

function lockMilestone(milestoneId) {
  lockedMilestones.push(milestoneId);
}

function unlockMilestone(milestoneId) {
  lockedMilestones.splice(lockedMilestones.indexOf(milestoneId), 1);
}

export default function(data) {
  const sendMilestone = makeSendMilestone(data.studentMilestonesUrl);

  function onMilestoneClick(ev) {
    const milestoneId = this.dataset.milestone;
    if (isMilestoneLocked(milestoneId)) {
      return;
    }
    lockMilestone(milestoneId);

    sendMilestone(milestoneId)
    .then(data => {
      const dateSpan = this.children[0];
      if (data.action === 'add') {
        dateSpan.classList.add('bg-primary', 'text-white');
      } else if (data.action === 'remove') {
        dateSpan.classList.remove('bg-primary', 'text-white');
      }
      unlockMilestone(milestoneId);
    });
  }

  on('click', '.milestone-cell', onMilestoneClick);

  $('#schools').DataTable({
    info: false,
    paging: false,
    searching: false
  });
}
