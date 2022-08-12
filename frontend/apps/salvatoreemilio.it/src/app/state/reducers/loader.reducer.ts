import { createEntityAdapter, EntityAdapter, EntityState } from '@ngrx/entity';
import { createReducer, on } from '@ngrx/store';
import * as LOADER_ACTIONS from '../actions/loader.actions';

export interface Loader {
  id: string;
  value: number;
}

export interface LoaderState extends EntityState<Loader> {
  loading: boolean;
}

export const LOADER_ADAPTER: EntityAdapter<Loader> =
  createEntityAdapter<Loader>({
    selectId: (loader) => loader.id,
  });

const INITIAL_LOADER_STATE: LoaderState = LOADER_ADAPTER.getInitialState({
  loading: false,
});

export const LOADER_REDUCER = createReducer(
  INITIAL_LOADER_STATE,
  on(LOADER_ACTIONS.LOADER_ON, (state, { key }) => {
    if (state.entities[key]) {
      return LOADER_ADAPTER.updateOne(
        {
          id: key,
          changes: {
            value: state.entities[key]!.value + 1,
          },
        },
        state
      );
    }
    return LOADER_ADAPTER.addOne(
      {
        id: key,
        value: 1,
      },
      state.loading ? state : { ...state, loading: true }
    );
  }),
  on(LOADER_ACTIONS.LOADER_OFF, (state, { key }) => {
    if (state.entities[key] == null) {
      console.error(`LOADER_OFF key '${key}' missing from state`);
      return state;
    }
    let value: number = state.entities[key]!.value - 1;
    if (value < 1) {
      return LOADER_ADAPTER.removeOne(
        key,
        state.ids.length > 1 ? state : { ...state, loading: false }
      );
    }
    return LOADER_ADAPTER.updateOne(
      {
        id: key,
        changes: {
          value: value,
        },
      },
      state
    );
  })
);
