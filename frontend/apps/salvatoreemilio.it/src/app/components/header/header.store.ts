import { Injectable } from '@angular/core';
import { ComponentStore } from '@ngrx/component-store';
import { Store } from '@ngrx/store';
import { Observable, switchMap } from 'rxjs';
import { SELECT_USER_PROFILE_PICTURE } from '../../app.state';

export interface HeaderState {
  profilePicture: string | undefined;
}

@Injectable()
export class HeaderStore extends ComponentStore<HeaderState> {
  constructor(
    private readonly headerStore: ComponentStore<HeaderState>,
    private store: Store
  ) {
    super({ profilePicture: undefined });
  }

  readonly profilePicture$: Observable<string | undefined> = this.select(
    (state) => state?.profilePicture
  );

  readonly setProfilePicture = this.updater(
    (state, profilePicture: string | undefined) => ({
      profilePicture: profilePicture,
    })
  );

  readonly changeProfilePicture$ = this.effect(() =>
    this.store
      .select(SELECT_USER_PROFILE_PICTURE)
      .pipe(
        switchMap((profiePicture) => [this.setProfilePicture(profiePicture)])
      )
  );
}
