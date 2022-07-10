import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import {
  catchError,
  from,
  map,
  mergeMap,
  of,
  pairwise,
  startWith,
  switchMap,
  tap,
} from 'rxjs';
import { GraphqlService } from '../../services/graphql.service';
import {
  SET_USER,
  LOAD_USER,
  LOAD_USER_ERROR,
  LOAD_PROJECTS,
} from '../actions';
import { User } from '../../models';
import { LOADER_OFF, LOADER_ON } from '../actions/loader.actions';
import { KeycloakService } from 'keycloak-angular';
import { environment } from 'apps/salvatoreemilio.it/src/environments/environment';

@Injectable()
export class UserEffects {
  constructor(
    private actions$: Actions,
    private store: Store,
    private graphqlService: GraphqlService,
    private keycloakService: KeycloakService
  ) {}

  load$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(LOAD_USER),
      map((action) => action.email),
      tap((email) => {
        this.store.dispatch(LOADER_ON({ key: 'LOAD USER' }));

        this.store.dispatch(LOADER_ON({ key: 'LOAD PROJECTS' }));
        this.store.dispatch(LOAD_PROJECTS({ email: email }));
      }),
      switchMap((email) =>
        this.graphqlService.watchUser(email).pipe(startWith(undefined))
      ),
      pairwise(),
      mergeMap((pair) => {
        if (!pair[1]) {
          return [];
        }
        if (!pair[0]) {
          this.store.dispatch(LOADER_OFF({ key: 'LOAD USER' }));
        }
        this.store.dispatch(LOADER_ON({ key: `WATCH USER` }));
        return of(SET_USER({ user: pair[1]?.data?.watchUser as User }));
      }),
      catchError(() => [LOADER_OFF({ key: 'WatchUser' }), LOAD_USER_ERROR()])
    );
  });

  loadError$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(LOAD_USER_ERROR),
      switchMap(() => from(this.keycloakService.getToken())),
      map((token) => JSON.parse(window.atob(token?.split('.')[1]))?.email),
      catchError(() => of(undefined)),
      switchMap((email: string | undefined) =>
        of(LOAD_USER({ email: email ?? environment.email }))
      )
    );
  });

  setUser$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(SET_USER),
      switchMap(() => of(LOADER_OFF({ key: 'WATCH USER' })))
    );
  });
}
