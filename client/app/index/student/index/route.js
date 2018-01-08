import Route from '@ember/routing/route';

import ENV from 'client/config/environment';

export default Route.extend({
  titleToken(model) {
    return model.get('fullName');
  },

  authorize(makeApplicationStatusCallback) {
    window.gapi.load('auth2', () => {
      const auth2 = window.gapi.auth2.init({
        client_id: ENV.APP.googleClientId,
        scope: 'https://www.googleapis.com/auth/drive.file'
      });
      auth2.grantOfflineAccess({prompt: 'consent'}).then((authResponse) => {
        const auth = this.store.createRecord('google-drive-auth', {
          code: authResponse.code
        });
        auth.save().then(makeApplicationStatusCallback);
      });
    });
  },

  makeApplicationStatus(student) {
    const applicationStatus = this.store.createRecord('application-status', { student });
    applicationStatus.save();
  },

  actions: {
    triggerExport(student) {
      this.store.findAll('google-drive-auth').then((authorizations) => {
        if (authorizations.get('length') === 0) {
          const makeApplicationStatusCallback = () => {
            this.makeApplicationStatus(student);
          };
          this.authorize(makeApplicationStatusCallback);
        } else {
          this.makeApplicationStatus(student);
        }
      });
    }
  }
});
