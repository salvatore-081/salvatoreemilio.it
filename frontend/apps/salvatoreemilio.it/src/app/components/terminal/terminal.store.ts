import { Injectable } from '@angular/core';
import { ComponentStore } from '@ngrx/component-store';
import { Store } from '@ngrx/store';
import { Observable, skipWhile, switchMap } from 'rxjs';
import { SELECT_USER } from '../../app.state';
import { User } from '../../models';

export interface TerminalState {
  user: User;
}

@Injectable()
export class TerminalStore extends ComponentStore<TerminalState> {
  constructor(private store: Store) {
    super({ user: { email: '' } });
  }

  readonly selectUser$: Observable<User> = this.select(
    (state) => state.user
  ).pipe(skipWhile((u) => u.email === ''));

  readonly setUser = this.updater((state, user: User) => ({
    ...state,
    user: user,
  }));

  private readonly userUpdate$ = this.effect(() =>
    this.store
      .select(SELECT_USER)
      .pipe(switchMap((user) => [this.setUser(user)]))
  );
}
