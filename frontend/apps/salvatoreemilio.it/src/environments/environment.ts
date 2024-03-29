// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  graphql: {
    httpLink: 'https://api.salvatoreemilio.it/graphql/',
    wsLink: 'wss://api.salvatoreemilio.it/graphql/',
  },
  rest: {
    url: `https://api.salvatoreemilio.it`,
  },
  auth: {
    url: `https://login.salvatoreemilio.it`,
    realm: 'se',
    clientId: 'frontend-auth',
  },
  email: 'info@salvatoreemilio.it',
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
