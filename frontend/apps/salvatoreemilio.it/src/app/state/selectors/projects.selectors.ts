import { PROJECTS_ADAPTER } from '../reducers/projects.reducer';

const { selectIds, selectEntities, selectAll, selectTotal } =
  PROJECTS_ADAPTER.getSelectors();

export const SELECT_PROJETS_ENTITIES = selectEntities;

export const SELECT_ALL_PROJECTS = selectAll;
