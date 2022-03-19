import { createAction, props } from '@ngrx/store';
import { User } from '../../models';

export const LOAD = createAction('[USER] LOAD', props<{ email: string }>());

export const SET_USER = createAction('[USER] SET', props<{ user: User }>());