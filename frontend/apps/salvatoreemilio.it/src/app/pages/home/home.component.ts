import { Component, OnDestroy, OnInit } from '@angular/core';
import {
  interval,
  map,
  Observable,
  of,
  reduce,
  Subject,
  switchMap,
  take,
  takeUntil,
  tap,
} from 'rxjs';
import { User } from '../../models';
import { HomeStore } from './home.store';

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  providers: [HomeStore],
})
export class HomeComponent implements OnInit, OnDestroy {
  destroy$: Subject<void> = new Subject<void>();
  user$: Observable<User | undefined> = this.homeStore.selectUser$;
  fullName$: Observable<string> = this.homeStore.selectFullName$;
  fullName: string = '';

  constructor(private homeStore: HomeStore) {}

  ngOnInit(): void {
    console.log('HomeComponent ngOnInit()');

    this.fullName$
      .pipe(
        takeUntil(this.destroy$),
        switchMap((v) => {
          let obs$: Observable<string> =
            this.fullName.length > 0
              ? interval(150).pipe(
                  take(this.fullName.length),

                  map(() => v),
                  tap(() => {
                    this.fullName = this.fullName.slice(0, -1);
                  }),
                  reduce((acc, curr) => (acc = curr))
                )
              : of(v);

          return obs$.pipe(
            switchMap((v) =>
              interval(150).pipe(
                take(v.length),
                map(() => v),
                tap(() => {
                  this.fullName = `${this.fullName}${v.charAt(
                    this.fullName.length
                  )}`;
                }),
                reduce((acc, curr) => (acc = curr))
              )
            )
          );
        })
      )
      .subscribe();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
