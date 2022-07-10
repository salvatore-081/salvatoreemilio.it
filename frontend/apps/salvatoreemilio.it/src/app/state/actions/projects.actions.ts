import { createAction, props } from '@ngrx/store';
import { Project, ProjectFeed } from '../../models';

export const LOAD_PROJECTS = createAction(
  '[PROJECTS] LOAD',
  props<{ email: string }>()
);

export const SET_PROJECTS = createAction(
  '[PROJECTS] SET',
  props<{ projects: Project[] }>()
);

export const PROJECTS_FEED = createAction(
  '[PROJECTS] FEED',
  props<{ feed: ProjectFeed | undefined }>()
);

export const LOAD_PROJECTS_ERROR = createAction('[PROJECTS] LOAD ERROR');
