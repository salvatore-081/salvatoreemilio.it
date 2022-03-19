import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { map, mergeMap, of, switchMap, tap } from 'rxjs';
import { GraphqlService } from '../../services/graphql.service';
import { SET_USER, LOAD } from '../actions';
import { User } from '../../models'

@Injectable()
export class UserEffects {
  constructor(
    private actions$: Actions,
    private store: Store,
    private graphqlService: GraphqlService
  ) { }

  load$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(LOAD),
      map(action => action.email),
      switchMap((email) => this.graphqlService.watchUser(email)),
      mergeMap(watchUser => of(SET_USER({ user: watchUser?.data?.watchUser as User })))
    )
  }, { dispatch: true })
}