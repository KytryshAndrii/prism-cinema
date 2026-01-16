import { createSlice, type PayloadAction} from "@reduxjs/toolkit";

type tUserState = {
  id: string | null;
  login: string | null;
  email: string | null;
  region: string | null;
  birthday: string | null;
  token: string | null;
  isUserSubscribed: boolean;
  isUserAdmin: boolean;
  isLoggedIn: boolean;
}

const initialState: tUserState = {
  id: null,
  login: null,
  email: null,
  region: null,
  birthday: null,
  token: null,
  isUserAdmin: false,
  isUserSubscribed: false,
  isLoggedIn: false,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    logIn: (
      _,
      action: PayloadAction<tUserState>
    ) => {
        return { ...action.payload };
    },
    logOut: () => initialState,
    
    updateUser: (
      state,
      action: PayloadAction<{ login?: string; email?: string }>
    ) => {
      if (action.payload.login) {
        state.login = action.payload.login;
      }
      if (action.payload.email) {
        state.email = action.payload.email;
      }
    },

    subscribe:  (state) => {
      state.isUserSubscribed = true;
    },

    unsubscribe:  (state) => {
      state.isUserSubscribed = false;
    },
  },
});

export const { logIn, logOut, updateUser, subscribe, unsubscribe } = userSlice.actions;
export default userSlice.reducer;
