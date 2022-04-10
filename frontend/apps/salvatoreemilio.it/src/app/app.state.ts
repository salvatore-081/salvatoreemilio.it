import { createFeatureSelector, createSelector } from '@ngrx/store';
import { UserState, USER_REDUCER } from './state';
import { LoaderState, LOADER_REDUCER } from './state/reducers/loader.reducer';
import { GET_LOADER_LOADING } from './state/selectors';

export const APP_REDUCERS = {
  user: USER_REDUCER,
  loader: LOADER_REDUCER,
};

const SELECT_USER_FEATURE = createFeatureSelector<UserState>('user');

const SELECT_LOADER_FEATURE = createFeatureSelector<LoaderState>('loader');

export const SELECT_USER = createSelector(
  SELECT_USER_FEATURE,
  (state: UserState) => state
);

export const SELECT_LOADER_LOADING = createSelector(
  SELECT_LOADER_FEATURE,
  GET_LOADER_LOADING
);
