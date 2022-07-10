import { createReducer, on } from '@ngrx/store';
import * as USER_ACTIONS from '../actions/user.actions';
import { User } from '../../models';

export interface UserState extends User {}

const USER_INITIAL_STATE: UserState = {
  email: '',
};

export const USER_REDUCER = createReducer(
  USER_INITIAL_STATE,
  on(USER_ACTIONS.LOAD_USER, (state, { email }) => ({
    ...state,
    email: email,
  })),
  on(USER_ACTIONS.LOAD_USER_ERROR, (_) => USER_INITIAL_STATE),
  on(USER_ACTIONS.SET_USER, (_, { user }) => user)
);
