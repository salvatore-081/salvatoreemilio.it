import { createAction, props } from '@ngrx/store';
import { User } from '../../models';

export const LOAD_USER = createAction(
  '[USER] LOAD',
  props<{ email: string }>()
);

export const LOAD_USER_ERROR = createAction('[USER] LOAD ERROR');

export const SET_USER = createAction('[USER] SET', props<{ user: User }>());
