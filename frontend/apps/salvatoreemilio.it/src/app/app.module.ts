import { APP_INITIALIZER, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppComponent } from './app.component';
import { environment } from '../environments/environment';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ApolloModule, APOLLO_OPTIONS } from 'apollo-angular';
import { ApolloLink, InMemoryCache } from '@apollo/client/core';
import { HttpLink, HttpLinkHandler } from 'apollo-angular/http';
import { split } from '@apollo/client/core';
import { getMainDefinition } from '@apollo/client/utilities';
import { StoreModule } from '@ngrx/store';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { APP_REDUCERS } from './app.state';
import { EffectsModule } from '@ngrx/effects';
import { UserEffects } from './state/effects';
import { AppRoutingModule } from './app-routing.module';
import { ComponentStore } from '@ngrx/component-store';
import { LoaderInterceptor } from './interceptors/loader.interceptor';
import { KeycloakAngularModule, KeycloakService } from 'keycloak-angular';
import { MessageService } from 'primeng/api';
import { ProjectsEffects } from './state/effects/projects.effects';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';
import { HeaderComponent } from './components/header/header.component';

function initializeKeycloak(keycloak: KeycloakService) {
  return () =>
    keycloak.init({
      config: {
        url: environment.auth.url,
        realm: environment.auth.realm,
        clientId: environment.auth.clientId,
      },
      initOptions: {
        onLoad: 'check-sso',
        silentCheckSsoRedirectUri:
          window.location.origin + '/assets/silent-check-sso.html',
        checkLoginIframe: true,
      },
      enableBearerInterceptor: true,
    });
}

const STANDALONE_COMPONENTS = [HeaderComponent];

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    KeycloakAngularModule,
    ApolloModule,
    HttpClientModule,
    StoreModule.forRoot(APP_REDUCERS),
    EffectsModule.forRoot([UserEffects, ProjectsEffects]),
    StoreDevtoolsModule.instrument({
      maxAge: 25,
      logOnly: environment.production,
      autoPause: true,
    }),
    ...STANDALONE_COMPONENTS,
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: LoaderInterceptor,
      multi: true,
    },
    {
      provide: APP_INITIALIZER,
      useFactory: initializeKeycloak,
      multi: true,
      deps: [KeycloakService],
    },
    {
      provide: APOLLO_OPTIONS,
      useFactory: (httpLink: HttpLink) => {
        const HTTP: HttpLinkHandler = httpLink.create({
          uri: environment.graphql.httpLink,
        });

        const WS: GraphQLWsLink = new GraphQLWsLink(
          createClient({
            url: environment.graphql.wsLink,
          })
        );

        const LINK: ApolloLink = split(
          ({ query }) => {
            const call = getMainDefinition(query);
            return (
              call.kind === 'OperationDefinition' &&
              call.operation === 'subscription'
            );
          },
          WS,
          HTTP
        );

        return {
          link: LINK,
          cache: new InMemoryCache({ addTypename: false }),
        };
      },
      deps: [HttpLink],
    },
    ComponentStore,
    MessageService,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
