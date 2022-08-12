import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { KeycloakService } from 'keycloak-angular';
import { catchError, first, from, map, of } from 'rxjs';
import { environment } from '../environments/environment';
import { LOAD_USER } from './state/actions/user.actions';

@Component({
  selector: 'root',
  template: `
    <header class="header-component"></header>
    <div class="router-outlet-container">
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [
    `
      .router-outlet-container {
        height: calc(100vh - 78px);
        overflow-y: scroll;
        overflow-x: hidden;
        max-width: 100vw;
      }
    `,
  ],
})
export class AppComponent implements OnInit {
  constructor(private store: Store, private keycloakService: KeycloakService) {}

  ngOnInit(): void {
    from(this.keycloakService.getToken())
      .pipe(
        map((token) =>
          token
            ? JSON.parse(window.atob(token?.split('.')[1]))?.email
            : undefined
        ),
        catchError((e) => {
          console.error(e);
          return of(undefined);
        }),
        first()
      )
      .subscribe((email: string | undefined) => {
        this.store.dispatch(LOAD_USER({ email: email ?? environment.email }));
      });
  }
}
