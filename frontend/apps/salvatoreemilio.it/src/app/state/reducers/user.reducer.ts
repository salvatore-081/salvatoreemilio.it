import { createReducer, on } from '@ngrx/store';
import * as USER_ACTIONS from '../actions/user.actions';
import { User } from '../../models';

export interface UserState extends User {}

const INITIAL_USER_STATE: UserState = {
  email: '',
};

export const USER_REDUCER = createReducer(
  INITIAL_USER_STATE,
  on(USER_ACTIONS.LOAD, (state, { email }) => ({ ...state, email: email })),
  on(USER_ACTIONS.LOAD_ERROR, (_) => INITIAL_USER_STATE),
  on(USER_ACTIONS.SET_USER, (_, { user }) => user)
);
