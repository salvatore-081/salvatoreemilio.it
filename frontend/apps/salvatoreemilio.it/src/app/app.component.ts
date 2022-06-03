import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { KeycloakService } from 'keycloak-angular';
import { catchError, first, from, map, of } from 'rxjs';
import { environment } from '../environments/environment';
import { LOAD } from './state/actions/user.actions';

@Component({
  selector: 'root',
  template: `
    <header class="header__component"></header>
    <router-outlet></router-outlet>
  `,
  styles: [
    `
      .header__component {
        position: sticky;
        top: 0;
      }
    `,
  ],
})
export class AppComponent implements OnInit {
  constructor(
    private http: HttpClient,
    private store: Store,
    private keycloakService: KeycloakService
  ) {}

  ngOnInit(): void {
    from(this.keycloakService.getToken())
      .pipe(
        map((token) => JSON.parse(window.atob(token?.split('.')[1]))?.email),
        catchError((e) => {
          console.error(e);
          return of(undefined);
        }),
        first()
      )
      .subscribe((email: string | undefined) => {
        this.store.dispatch(LOAD({ email: email ?? environment.email }));
      });
  }
}
