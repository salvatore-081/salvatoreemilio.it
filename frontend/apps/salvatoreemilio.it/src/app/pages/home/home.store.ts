import { Injectable } from '@angular/core';
import { ComponentStore } from '@ngrx/component-store';
import { Store } from '@ngrx/store';
import { first, Observable, Subject, switchMap, take, tap } from 'rxjs';
import { User } from '../../models';
import { GraphqlService } from '../../services/graphql.service';
import { SELECT_USER } from '../../app.state';
import { MessageService } from 'primeng/api';
import { HttpClient } from '@angular/common/http';

export interface HomeState {
  user: User | undefined;
  fullName: string;
}

@Injectable()
export class HomeStore extends ComponentStore<HomeState> {
  constructor(private store: Store) {
    super({ user: undefined, fullName: '' });
  }

  readonly selectUser$: Observable<User | undefined> = this.select(
    (s) => s.user
  );

  readonly selectFullName$: Observable<string> = this.select((s) => s.fullName);

  private readonly updateUser = this.updater((state, user: User) => {
    return {
      ...state,
      user: user,
    };
  });

  private readonly updateFullName = this.updater((state, fullName: string) => {
    return fullName === state.fullName
      ? state
      : {
          ...state,
          fullName: fullName,
        };
  });

  private readonly userUpdate$ = this.effect(() =>
    this.store
      .select(SELECT_USER)
      .pipe(
        switchMap((user) => [
          this.updateUser(user),
          this.updateFullName(
            this.getFullName(user.email, user?.name, user?.surname)
          ),
        ])
      )
  );

  private getFullName(email: string, name?: string, surname?: string): string {
    let fullName: string = '';
    if (name && name?.length > 0) {
      fullName = `${name}`;
    }

    if (surname && surname?.length > 0) {
      fullName = fullName.length > 0 ? `${fullName} ${surname}` : `${surname}`;
    }

    return fullName.length > 0 ? fullName : email;
  }
}
