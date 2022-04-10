export const environment = {
  production: true,
  graphql: {
    httpLink: 'https://api.salvatoreemilio.it/graphql/',
    wsLink: 'wss://api.salvatoreemilio.it/graphql/',
  },
  auth: {
    url: `https://login.salvatoreemilio.it/auth`,
    realm: 'se',
    clientId: 'frontend-auth',
  },
  email: 'info@salvatoreemilio.it',
};
