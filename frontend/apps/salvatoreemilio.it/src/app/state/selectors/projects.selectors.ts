import { ProjectsState, PROJECTS_ADAPTER } from '../reducers/projects.reducer';

const { selectIds, selectEntities, selectAll, selectTotal } =
  PROJECTS_ADAPTER.getSelectors();

export const selectProjectsInit = (state: ProjectsState) => state.init;

export const selectProjectsEntities = selectEntities;

export const selectAllProjects = selectAll;
