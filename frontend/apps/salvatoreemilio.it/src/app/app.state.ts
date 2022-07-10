import { createFeatureSelector, createSelector } from '@ngrx/store';
import { User } from './models';
import { UserState, USER_REDUCER } from './state';
import { LoaderState, LOADER_REDUCER } from './state/reducers/loader.reducer';
import {
  ProjectsState,
  PROJECTS_REDUCER,
} from './state/reducers/projects.reducer';
import { GET_LOADER_LOADING } from './state/selectors';

export const APP_REDUCERS = {
  user: USER_REDUCER,
  loader: LOADER_REDUCER,
  projects: PROJECTS_REDUCER,
};

const SELECT_USER_FEATURE = createFeatureSelector<UserState>('user');

const SELECT_LOADER_FEATURE = createFeatureSelector<LoaderState>('loader');

const SELECT_PROJECTS_FEATURE =
  createFeatureSelector<ProjectsState>('projects');

export const SELECT_USER = createSelector(
  SELECT_USER_FEATURE,
  (state: UserState) => state
);

export const SELECT_USER_PROFILE_PICTURE = createSelector(
  SELECT_USER,
  (user: User) => user?.profilePicture
);

export const SELECT_LOADER_LOADING = createSelector(
  SELECT_LOADER_FEATURE,
  GET_LOADER_LOADING
);
