import { createFeatureSelector, createSelector } from "@ngrx/store";
import { UserState, USER_REDUCER } from "./state";

export const APP_REDUCERS = {
  user: USER_REDUCER
}

const SELECT_USER_STATE = createFeatureSelector<UserState>('user')

export const SELECT_USER = createSelector(SELECT_USER_STATE, (state: UserState) => state)



