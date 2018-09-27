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

function makeSendSchoolApplication(studentSchoolApplicationsUrl) {
  return function(schoolApplicationId) {
    schoolApplicationId = parseInt(schoolApplicationId, 10)
    return fetch(studentSchoolApplicationsUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': utils.getCsrfToken()
      },
      body: JSON.stringify({'school_application': schoolApplicationId})
    })
    .then(checkStatus)
    .then(parseJSON)
  }
}

let lockedSchools = [];

function isSchoolLocked(schoolId) {
  return lockedSchools.includes(schoolId);
}

function lockSchool(schoolId) {
  lockedSchools.push(schoolId);
}

function unlockSchool(schoolId) {
  lockedSchools.splice(lockedSchools.indexOf(schoolId), 1);
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

  const sendSchoolApplication = makeSendSchoolApplication(data.studentSchoolApplicationsUrl);

  function onSchoolApplicationClick(ev) {
    ev.preventDefault();
    const schoolId = this.dataset.school;
    if (isSchoolLocked(schoolId)) {
      return;
    }
    lockSchool(schoolId);

    const schoolApplicationId = this.dataset.school_application;
    sendSchoolApplication(schoolApplicationId)
    .then(data => {
      const schoolNodes = document.querySelectorAll(`.school-${schoolId}-btn`);
      if (data.action === 'add') {
        schoolNodes.forEach(schoolNode => {
          schoolNode.classList.add('btn-outline-secondary');
          schoolNode.classList.remove('btn-primary', 'btn-secondary');
        });
        // Style the button clicked as the new selected school application.
        this.classList.add('btn-primary');
        this.classList.remove('btn-secondary', 'btn-outline-secondary');
      } else if (data.action === 'remove') {
        schoolNodes.forEach(schoolNode => {
          schoolNode.classList.add('btn-secondary');
          schoolNode.classList.remove('btn-primary', 'btn-outline-secondary');
        });
      }
      unlockSchool(schoolId);
    });
  }

  on('click', '.school-application-btn', onSchoolApplicationClick);

  $('#schools').DataTable({
    info: false,
    paging: false,
    searching: false
  });
}
