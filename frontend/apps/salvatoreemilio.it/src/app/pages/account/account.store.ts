import { Injectable } from '@angular/core';
import { ComponentStore } from '@ngrx/component-store';
import { Store } from '@ngrx/store';
import { first, Observable, switchMap, take } from 'rxjs';
import { Project, User } from '../../models';
import { GraphqlService } from '../../services/graphql.service';
import {
  SELECT_PROJECTS,
  SELECT_PROJECTS_INIT,
  SELECT_USER,
} from '../../app.state';
import { MessageService } from 'primeng/api';
import { UtilsService } from '../../services/utils.service';

export interface AccountState extends User {
  emailLoading: boolean;
  nameLoading: boolean;
  surnameLoading: boolean;
  phoneNumberLoading: boolean;
  locationLoading: boolean;
  profilePictureLoading: boolean;
  projects: Project[];
  projectsInit: boolean;
}

@Injectable()
export class AccountStore extends ComponentStore<AccountState> {
  constructor(
    private graphqlService: GraphqlService,
    private store: Store,
    private messageService: MessageService,
    private utilsService: UtilsService
  ) {
    super({
      email: '',
      emailLoading: true,
      nameLoading: false,
      surnameLoading: false,
      phoneNumberLoading: false,
      locationLoading: false,
      profilePictureLoading: true,
      projects: [],
      projectsInit: false,
    });
  }

  readonly emailLoading$: Observable<boolean> = this.select(
    (state) => state.emailLoading
  ).pipe(take(2));

  readonly email$: Observable<string> = this.select((s) => s.email);

  readonly name$: Observable<string | undefined> = this.select((s) => s?.name);

  readonly nameLoading$: Observable<boolean> = this.select(
    (s) => s.nameLoading
  );

  readonly surname$: Observable<string | undefined> = this.select(
    (s) => s?.surname
  );

  readonly surnameLoading$: Observable<boolean> = this.select(
    (s) => s.surnameLoading
  );

  readonly phoneNumber$: Observable<string | undefined> = this.select(
    (s) => s?.phoneNumber
  );

  readonly phoneNumberLoading$: Observable<boolean> = this.select(
    (s) => s.phoneNumberLoading
  );

  readonly location$: Observable<string | undefined> = this.select(
    (s) => s?.location
  );

  readonly locationLoading$: Observable<boolean> = this.select(
    (s) => s.locationLoading
  );

  readonly profilePicture$: Observable<string | undefined> = this.select(
    (s) => s?.profilePicture
  );

  readonly profilePictureLoading$: Observable<boolean> = this.select(
    (s) => s.profilePictureLoading
  );

  readonly selectProjects$: Observable<Project[]> = this.select(
    (s) => s.projects
  );

  readonly selectProjectsInit$: Observable<boolean> = this.select(
    (s) => s.projectsInit
  );

  private readonly updateProjects = this.updater(
    (state, projects: Project[]) => {
      return {
        ...state,
        projects: projects,
      };
    }
  );

  private readonly updateProjectsInit = this.updater((state, init: boolean) => {
    return {
      ...state,
      projectsInit: init,
    };
  });

  private readonly updateUser = this.updater((state, user: User) => {
    let s: Partial<AccountState> = {};
    (Object.keys(user) as Array<keyof User>).forEach((k) => {
      if (user[k] !== state[k]) {
        s[k] = user[k];
        s[`${k}Loading`] = false;
      }
    });

    return {
      ...state,
      ...s,
    };
  });

  readonly updateProfilePicture = this.updater((state, url: string) => {
    this.utilsService
      .readBlob(url)
      .pipe(
        switchMap((blob: string) =>
          this.graphqlService.updateUserProfilePicture(state.email, blob)
        ),
        first()
      )
      .subscribe({
        next: (_) =>
          this.messageService.add({
            severity: 'success',
            summary: 'Profile picture modificata!',
          }),
        error: (_) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Ops... qualcosa è andato storto!',
          });
          this.updateProfilePictureHandleError();
        },
      });
    return {
      ...state,
      profilePictureLoading: true,
    };
  });

  private updateProfilePictureHandleError = this.updater((state) => {
    return {
      ...state,
      profilePictureLoading: false,
    };
  });

  readonly updateName = this.updater((state, name: string) => {
    this.graphqlService
      .updateUserName(state.email, name)
      .pipe(first())
      .subscribe({
        next: (_) =>
          this.messageService.add({
            severity: 'success',
            summary: 'Name modificato!',
          }),
        error: (_) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Ops... qualcosa è andato storto!',
          });
          this.updateNameHandleError();
        },
      });

    return {
      ...state,
      nameLoading: true,
    };
  });

  private readonly updateNameHandleError = this.updater((state) => {
    return {
      ...state,
      nameLoading: false,
    };
  });

  readonly updateSurname = this.updater((state, surname: string) => {
    this.graphqlService
      .updateUserSurname(state.email, surname)
      .pipe(first())
      .subscribe({
        next: (_) =>
          this.messageService.add({
            severity: 'success',
            summary: 'Surname modificato!',
          }),
        error: (_) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Ops... qualcosa è andato storto!',
          });
          this.updateSurnameHandleError();
        },
      });

    return {
      ...state,
      surnameLoading: true,
    };
  });

  private readonly updateSurnameHandleError = this.updater((state) => {
    return {
      ...state,
      surnameLoading: false,
    };
  });

  readonly updatePhoneNumber = this.updater((state, phoneNumber: string) => {
    this.graphqlService
      .updateUserPhoneNumber(state.email, phoneNumber)
      .pipe(first())
      .subscribe({
        next: (_) =>
          this.messageService.add({
            severity: 'success',
            summary: 'Phone number modificato!',
          }),
        error: (_) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Ops... qualcosa è andato storto!',
          });
          this.updatePhoneNumberHandleError();
        },
      });

    return {
      ...state,
      phoneNumberLoading: true,
    };
  });

  private readonly updatePhoneNumberHandleError = this.updater((state) => {
    return {
      ...state,
      phoneNumberLoading: false,
    };
  });

  readonly updateLocation = this.updater((state, location: string) => {
    this.graphqlService
      .updateUserLocation(state.email, location)
      .pipe(first())
      .subscribe({
        next: (_) =>
          this.messageService.add({
            severity: 'success',
            summary: 'Location modificata!',
          }),
        error: (_) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Ops... qualcosa è andato storto!',
          });
          this.updateLocationHandleError();
        },
      });

    return {
      ...state,
      locationLoading: true,
    };
  });

  private readonly updateLocationHandleError = this.updater((state) => {
    return {
      ...state,
      locationLoading: false,
    };
  });

  private readonly userUpdate$ = this.effect(() =>
    this.store
      .select(SELECT_USER)
      .pipe(switchMap((user) => [this.updateUser(user)]))
  );

  private readonly projectsFeed$ = this.effect(() =>
    this.store
      .select(SELECT_PROJECTS)
      .pipe(switchMap((projects) => [this.updateProjects(projects)]))
  );

  private readonly projectsInit$ = this.effect(() =>
    this.store
      .select(SELECT_PROJECTS_INIT)
      .pipe(switchMap((init) => [this.updateProjectsInit(init)]))
  );
}
