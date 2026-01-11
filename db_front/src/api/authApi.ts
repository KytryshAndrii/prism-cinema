import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

type tRegisterRequest = {
  login: string;
  email: string;
  password: string;
  dateOfBirth: string;
}

type tLoginRequest = {
  login: string;
  password: string;
}

type tAuthResponse = {
  id: string;
  login: string;
  email: string;
  token: string;
}

type tRootState = {
    user: {
        id: string;
        login: string;
        email: string;
        token: string;
    }
}

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_PRISM_CINEMA_BACKEND,
    prepareHeaders: (headers, { getState }) => {
        const token = (getState() as tRootState).user.token;
        if (token) {
            headers.set("Authorization", `Bearer ${token}`);
        }
        return headers;
}
  }),
  
  endpoints: (builder) => ({

    registerUser: builder.mutation<tAuthResponse, tRegisterRequest>({
       query: (body) => ({
        url: "/register",
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }),
    }),

    loginUser: builder.mutation<tAuthResponse, tLoginRequest>({
       query: (body) => ({
        url: "/login",
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }),
    }),
  }),
});

export const { useRegisterUserMutation, useLoginUserMutation } = authApi;
