import { APP_INITIALIZER, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppComponent } from './app.component';
import { environment } from '../environments/environment';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ApolloModule, APOLLO_OPTIONS } from 'apollo-angular';
import { ApolloLink, InMemoryCache } from '@apollo/client/core';
import { HttpLink, HttpLinkHandler } from 'apollo-angular/http';
import { WebSocketLink } from '@apollo/client/link/ws';
import { split } from '@apollo/client/core';
import { getMainDefinition } from '@apollo/client/utilities';
import { StoreModule } from '@ngrx/store';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { APP_REDUCERS } from './app.state';
import { EffectsModule } from '@ngrx/effects';
import { UserEffects } from './state/effects';
import { AppRoutingModule } from './app-routing.module';
import { HeaderComponent } from './components/header/header.component';
import { ComponentStore } from '@ngrx/component-store';
import { AvatarModule } from 'primeng/avatar';
import { MenuModule } from 'primeng/menu';
import { ProgressBarModule } from 'primeng/progressbar';
import { LoaderInterceptor } from './interceptors/loader.interceptor';
import { KeycloakAngularModule, KeycloakService } from 'keycloak-angular';
import { ButtonModule } from 'primeng/button';
import { ReactiveComponentModule } from '@ngrx/component';
import { MessageService } from 'primeng/api';
import { SkeletonModule } from 'primeng/skeleton';
import { ProjectsEffects } from './state/effects/projects.effects';

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

const PRIMENG_MODULES = [
  AvatarModule,
  MenuModule,
  ProgressBarModule,
  ButtonModule,
  SkeletonModule,
];

@NgModule({
  declarations: [AppComponent, HeaderComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    KeycloakAngularModule,
    ReactiveComponentModule,
    ApolloModule,
    HttpClientModule,
    StoreModule.forRoot(APP_REDUCERS),
    EffectsModule.forRoot([UserEffects, ProjectsEffects]),
    StoreDevtoolsModule.instrument({
      maxAge: 25,
      logOnly: environment.production,
      autoPause: true,
    }),
    PRIMENG_MODULES,
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

        const WS: WebSocketLink = new WebSocketLink({
          uri: environment.graphql.wsLink,
          options: {
            reconnect: true,
          },
        });

        const LINK: ApolloLink = split(
          ({ query }) => {
            const { kind, operation }: { kind: string; operation?: string } =
              getMainDefinition(query);
            return (
              kind === 'OperationDefinition' && operation === 'subscription'
            );
          },
          WS,
          HTTP
        );

        return {
          cache: new InMemoryCache(),
          link: LINK,
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
