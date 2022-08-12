import { createReducer, on } from '@ngrx/store';
import * as PROJECTS_ACTIONS from '../actions/projects.actions';
import { Project } from '../../models';
import { createEntityAdapter, EntityAdapter, EntityState } from '@ngrx/entity';

export interface ProjectsState extends EntityState<Project> {
  init: boolean;
}

export const PROJECTS_ADAPTER: EntityAdapter<Project> =
  createEntityAdapter<Project>({
    selectId: (project: Project) => project.id,
    sortComparer: (a: Project, b: Project) => (a.index < b.index ? -1 : +1),
  });

const PROJECTS_INITIAL_STATE: ProjectsState = PROJECTS_ADAPTER.getInitialState({
  init: false,
});

export const PROJECTS_REDUCER = createReducer(
  PROJECTS_INITIAL_STATE,
  on(PROJECTS_ACTIONS.LOAD_PROJECTS, (state, { email }) =>
    PROJECTS_ADAPTER.removeAll({ ...state, init: false })
  ),
  on(PROJECTS_ACTIONS.PROJECTS_FEED, (state, { feed }) => {
    if (
      (!feed?.new_val || feed!.new_val!.id === '') &&
      (!feed?.old_val || feed!.old_val!.id === '')
    ) {
      return { ...state, ...(!state.init && { init: true }) };
    }
    if (!feed?.old_val || feed!.old_val!.id === '') {
      return PROJECTS_ADAPTER.addOne(feed!.new_val!, {
        ...state,
        ...(!state.init && { init: true }),
      });
    }
    if (!feed?.new_val || feed!.new_val!.id === '') {
      return PROJECTS_ADAPTER.removeOne(feed.old_val.id!, { ...state });
    }
    return PROJECTS_ADAPTER.updateOne(
      {
        id: feed.old_val.id!,
        changes: {
          ...feed.new_val!,
        },
      },
      { ...state }
    );
  })
);
