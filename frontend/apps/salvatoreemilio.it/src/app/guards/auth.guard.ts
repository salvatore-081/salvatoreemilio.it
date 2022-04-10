import { UnregisteredTaskException } from '@angular-devkit/schematics';
import { Injectable } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  CanActivate,
  Params,
  Router,
  RouterStateSnapshot,
} from '@angular/router';
import { Store } from '@ngrx/store';
import { KeycloakAuthGuard, KeycloakService } from 'keycloak-angular';
import { env } from 'process';
import {
  catchError,
  finalize,
  firstValueFrom,
  from,
  lastValueFrom,
  map,
  Observable,
  of,
  skipWhile,
  switchMap,
  tap,
} from 'rxjs';
import { environment } from '../../environments/environment';
import { SELECT_USER } from '../app.state';
import { LOAD, UserState } from '../state';
import { LOADER_OFF, LOADER_ON } from '../state/actions/loader.actions';
// import { RequiredRole } from './required-role';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard extends KeycloakAuthGuard implements CanActivate {
  constructor(
    protected override router: Router,
    protected override keycloakAngular: KeycloakService,
    private store: Store
  ) {
    super(router, keycloakAngular);
  }

  private readonly login$: Observable<boolean> = this.store
    .select(SELECT_USER)
    .pipe(
      tap(() => this.store.dispatch(LOADER_ON({ key: 'LOGIN' }))),
      // LOADER_OFF is not needed since
      // login() will redirect to a new domain
      switchMap((user) =>
        from(
          this.keycloakAngular.login({
            redirectUri: `${window.location.origin}/account`,
            loginHint: user.email === environment.email ? user.email : 'demo',
          })
        )
      ),
      map(() => true),
      catchError(() => of(false))
    );

  isAccessAllowed(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Promise<boolean> {
    return firstValueFrom(
      of(this.store.dispatch(LOADER_ON({ key: 'LOGIN' }))).pipe(
        finalize(() => this.store.dispatch(LOADER_OFF({ key: 'LOGIN' }))),
        switchMap(() => this.store.select(SELECT_USER)),
        switchMap((user: UserState) => {
          if (!this.authenticated) {
            if (
              (route.queryParams as Params)['email']?.length > 0 &&
              (route.queryParams as Params)['email'] !== user.email
            ) {
              this.store.dispatch(
                LOAD({
                  email: (route.queryParams as Params)['email'] as string,
                })
              );
              return this.store.select(SELECT_USER).pipe(
                skipWhile((user: UserState) => user.email === ''),
                map((user: UserState) => user.email),
                switchMap((email: string) =>
                  from(
                    this.keycloakAngular.login({
                      redirectUri: `${window.location.origin}/account`,
                      loginHint: email === environment.email ? email : 'demo',
                    })
                  )
                ),
                map(() => true),
                catchError(() => of(false))
              );
            }

            return from(
              this.keycloakAngular.login({
                redirectUri: `${window.location.origin}/account`,
                loginHint:
                  user.email === environment.email ? user.email : 'demo',
              })
            ).pipe(
              map(() => true),
              catchError(() => of(false))
            );
          }

          return from(this.keycloakAngular.getToken()).pipe(
            map(
              (token) =>
                JSON.parse(window.atob(token?.split('.')[1]))?.email ===
                user.email
            ),
            switchMap((value: boolean) => {
              if (value) {
                return of(value);
              }
              this.keycloakAngular.clearToken();
              return of(
                this.keycloakAngular.logout(
                  `${window.location.origin}/account?email=${user.email}`
                )
              ).pipe(map(() => false));
            }),
            catchError(() => of(false))
          );
        })
      )
    );

    return new Promise((resolve, reject) => {
      if (!this.authenticated) {
        this.keycloakAngular
          .login({ redirectUri: `${window.location.origin}/account` })
          .catch((e) => console.error(e));
        return reject(false);
      }

      // const requiredRoles: RequiredRole[] = route.data.roles;

      /**
       * 'this.roles' contains all the roles of the user regardless of the scope mappings
       * so if the application defines role A and in the application is mapped role from another client,
       * let's say view-profile from account client, this.roles is ['A', 'view-profile']
       * and we lose the information about which client has associated a certain role.
       *
       * If we use the method 'hasResourceRole' we are able to discriminate also the client which
       * has certain role associated and we can ask
       * hasResourceRole('view-profile', 'account')?
       * If we don't specify the second parameter the clientId is used automatically
       *
       * We can use this.roles for a coarse grained check (e.g. has any roles?)
       * and the other method for a more fine grained and clash free check of the roles
       */

      // if (!requiredRoles || requiredRoles.length === 0) {
      //   return resolve(true);
      // } else {
      //   let hasAllRequiredRoles;

      //   if (!this.roles || this.roles.length === 0) {
      //     hasAllRequiredRoles = false;
      //   } else {
      //     hasAllRequiredRoles = requiredRoles.every(reqRole => RequiredRole.hasRequiredRole(this.keycloakAngular, reqRole));
      //   }

      //   resolve(hasAllRequiredRoles);
      // }
      resolve(true);
    });
  }
}
