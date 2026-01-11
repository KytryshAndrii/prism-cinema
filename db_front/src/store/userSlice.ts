import { createSlice, type PayloadAction} from "@reduxjs/toolkit";

type tUserState = {
  id: string | null;
  login: string | null;
  email: string | null;
  token: string | null;
  isLoggedIn: boolean;
}

const initialState: tUserState = {
  id: null,
  login: null,
  email: null,
  token: null,
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
  },
});

export const { logIn, logOut } = userSlice.actions;
export default userSlice.reducer;
