import { Injectable } from '@angular/core';
import { ComponentStore } from '@ngrx/component-store';
import { Store } from '@ngrx/store';
import { environment } from 'apps/salvatoreemilio.it/src/environments/environment';
import { map, Observable, skipWhile, switchMap } from 'rxjs';
import { User } from '../../models';
import { GraphqlService } from '../../services/graphql.service';
import { SELECT_USER } from '../../app.state';
import { LOAD } from '../../state';

export interface AccountsUser extends User {
  selected: boolean;
  current: boolean;
}

export interface AccountsState {
  loading: boolean;
  userList: AccountsUser[];
}

@Injectable()
export class AccountsStore extends ComponentStore<AccountsState> {
  constructor(private graphqlService: GraphqlService, private store: Store) {
    super({
      loading: true,
      userList: [],
    });
    this.store
      .select(SELECT_USER)
      .pipe(
        skipWhile((user) => user.email === ''),
        switchMap((user: User) =>
          this.graphqlService.getUserList().pipe(
            map((getUserList) =>
              getUserList.data?.getUserList?.userList
                ?.map((u) => ({
                  ...u,
                  selected: u.email === user.email,
                  current: u.email === user.email,
                }))
                ?.sort((a, b) => (a.email === environment.email ? -1 : 1))
            )
          )
        )
      )
      .subscribe((v) => this.load(v ?? []));
  }

  readonly loading$: Observable<boolean> = this.select(
    (state) => state.loading
  ).pipe(skipWhile((init) => init == null));

  readonly userList$: Observable<AccountsUser[]> = this.select(
    (state) => state.userList
  ).pipe(skipWhile((users) => users == null));

  private readonly load = this.updater((state, userList: AccountsUser[]) => ({
    loading: false,
    userList: userList,
  }));

  readonly selectUser = this.updater((state, email: string) => ({
    ...state,
    userList: state.userList.map((u) => ({
      ...u,
      selected: u.email === email,
    })),
  }));

  readonly switchCurrentAccount = this.updater((state, email: string) => {
    this.store.dispatch(LOAD({ email: email }));
    return {
      ...state,
      userList: state.userList.map((u) => ({
        ...u,
        current: u.email === email,
      })),
    };
  });

  // readonly changeselectedUser = this.effect(() =>
  //   this.store
  //     .select(SELECT_USER)
  //     .pipe(switchMap((user) => [this.setselectedUser(user)]))
  // );
}
