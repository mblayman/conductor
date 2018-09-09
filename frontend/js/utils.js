function getCsrfToken() {
  let crumbles = document.cookie.split(';');
  for (let crumble of crumbles) {
    let pair = crumble.split('=');
    if (pair[0].trim() === 'csrftoken') {
      return decodeURIComponent(pair[1]);
    }
  }
}

export default {
  getCsrfToken
}
