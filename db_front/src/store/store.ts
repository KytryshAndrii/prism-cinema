import { configureStore } from '@reduxjs/toolkit';
import userReducer from './userSlice';
import filmReducer from './filmSlice';
import { authApi } from '../api/authApi';
import { setupListeners } from '@reduxjs/toolkit/query';

export const store = configureStore({
  reducer: {
    user: userReducer,
    film: filmReducer,
    [authApi.reducerPath]: authApi.reducer,
  },
  middleware: getDefaultMiddleware => getDefaultMiddleware().concat(authApi.middleware),
});

setupListeners(store.dispatch);

export type AppState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
