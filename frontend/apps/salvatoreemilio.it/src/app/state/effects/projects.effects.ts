import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { map, mergeMap, of, pairwise, startWith, switchMap } from 'rxjs';
import { GraphqlService } from '../../services/graphql.service';
import { LOAD_PROJECTS, PROJECTS_FEED } from '../actions';
import { LOADER_OFF, LOADER_ON } from '../actions/loader.actions';

@Injectable()
export class ProjectsEffects {
  constructor(
    private actions$: Actions,
    private store: Store,
    private graphqlService: GraphqlService
  ) {}

  clear$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(LOAD_PROJECTS),
      map((action) => action.email),
      switchMap((email: string) =>
        this.graphqlService.watchProjects(email).pipe(startWith(undefined))
      ),
      pairwise(),
      mergeMap((pair) => {
        if (!pair[1]) {
          return [];
        }
        if (!pair[0]) {
          this.store.dispatch(LOADER_OFF({ key: 'LOAD PROJECTS' }));
        }
        this.store.dispatch(LOADER_ON({ key: `PROJECTS FEED` }));
        return of(PROJECTS_FEED({ feed: pair[1]?.data?.projectFeed }));
      })
    );
  });

  feed$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(PROJECTS_FEED),
      switchMap(() => of(LOADER_OFF({ key: 'PROJECTS FEED' })))
    );
  });
}
