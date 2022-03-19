import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { environment } from '../environments/environment';
import { HttpClientModule } from '@angular/common/http';
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

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ApolloModule,
    HttpClientModule,
    StoreModule.forRoot(APP_REDUCERS),
    EffectsModule.forRoot([UserEffects]),
    StoreDevtoolsModule.instrument({
      maxAge: 25,
      logOnly: environment.production,
      autoPause: true,
    })
  ],
  providers: [
    {
      provide: APOLLO_OPTIONS,
      useFactory: (httpLink: HttpLink) => {
        const HTTP: HttpLinkHandler = httpLink.create({ uri: environment.graphql.httpLink })

        const WS: WebSocketLink = new WebSocketLink({
          uri: environment.graphql.wsLink,
          options: {
            reconnect: true,
          },
        });

        const LINK: ApolloLink = split(
          ({ query }) => {
            const { kind, operation }: { kind: string, operation?: string } = getMainDefinition(query);
            return (
              kind === 'OperationDefinition' && operation === 'subscription'
            );
          },
          WS,
          HTTP,
        )

        return {
          cache: new InMemoryCache(),
          link: LINK
        }
      },
      deps: [HttpLink]
    }
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
