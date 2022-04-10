import { Injectable } from '@angular/core';
import { ComponentStore } from '@ngrx/component-store';
import { Store } from '@ngrx/store';
import { Observable, skipWhile, switchMap } from 'rxjs';
import { SELECT_USER } from '../../app.state';
import { User } from '../../models';

export interface HeaderState {
  selectedUser: User;
}

@Injectable()
export class HeaderStore extends ComponentStore<HeaderState> {
  constructor(
    private readonly headerStore: ComponentStore<HeaderState>,
    private store: Store
  ) {
    super({ selectedUser: { email: '' } });
  }

  readonly selectedUser$: Observable<User> = this.select(
    (state) => state.selectedUser
  ).pipe(skipWhile((selectedUser) => selectedUser.email === ''));

  readonly setSelectedUser = this.updater((state, user: User) => ({
    selectedUser: user,
  }));

  readonly changeSelectedUser = this.effect(() =>
    this.store
      .select(SELECT_USER)
      .pipe(switchMap((user) => [this.setSelectedUser(user)]))
  );
}
