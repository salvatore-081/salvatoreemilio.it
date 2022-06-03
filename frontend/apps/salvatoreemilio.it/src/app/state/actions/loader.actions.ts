import { createAction, props } from "@ngrx/store";

export const LOADER_ON = createAction('[LOADER] ON', props<{ key: string }>());

export const LOADER_OFF = createAction('[LOADER] OFF', props<{ key: string }>());

