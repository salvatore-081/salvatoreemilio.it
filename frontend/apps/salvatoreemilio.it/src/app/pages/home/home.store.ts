import { Injectable } from '@angular/core';
import { ComponentStore } from '@ngrx/component-store';
import { Store } from '@ngrx/store';
import { Observable, switchMap } from 'rxjs';
import { Project, User } from '../../models';
import {
  SELECT_PROJECTS,
  SELECT_PROJECTS_INIT,
  SELECT_USER,
} from '../../app.state';

export interface HomeState {
  user: User | undefined;
  fullName: string;
  projects: Project[];
  projectsInit: boolean;
}

@Injectable()
export class HomeStore extends ComponentStore<HomeState> {
  constructor(private store: Store) {
    super({
      user: undefined,
      fullName: '',
      projects: [],
      projectsInit: false,
    });
  }

  readonly selectUser$: Observable<User | undefined> = this.select(
    (s) => s.user
  );

  readonly selectProjects$: Observable<Project[] | undefined> = this.select(
    (s) => s.projects
  );

  readonly selectProjectsInit$: Observable<boolean> = this.select(
    (s) => s.projectsInit
  );

  readonly selectFullName$: Observable<string> = this.select((s) => s.fullName);

  private readonly updateUser = this.updater((state, user: User) => {
    return {
      ...state,
      user: user,
    };
  });

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
