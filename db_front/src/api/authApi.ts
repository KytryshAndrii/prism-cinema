import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { tAuthResponse, tFavMovieRequest, tLoginRequest, tMovieDetailsResponse, tMovieResponse, tRegisterRequest, tRootState, tSearchMoviesResponse, tSubscriptionsPlansResponse, tUpdateUserDataResponse, tUserSubscriptionPlanMetaDataResponse, tUserToPlanSubscriptionRequest} from "../types/authTypes";

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
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }),
    }),

    loginUser: builder.mutation<tAuthResponse, tLoginRequest>({
       query: (body) => ({
        url: "/login",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }),
    }),

    updateUserProfile: builder.mutation<void, tUpdateUserDataResponse>({
      query: ({ userId, ...body }) => ({
        url: `/update/user/${userId}`,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }),
    }),

    searchMovies: builder.query<tSearchMoviesResponse, string>({
      query: (query) => ({
        url: `/search/movies?query=${encodeURIComponent(query)}`,
        method: "GET",
      }),
    }),
    
    getMovies: builder.query<tMovieResponse[], void>({
      query: () => ({
      url: "/movies",
      method: "GET",
      }),
    }),
    
    getMovieDetails: builder.query<tMovieDetailsResponse, string>({
      query: (movieId) => ({
        url: `/movie_details/${movieId}`,
        method: "GET",
      }),
    }),

    getSubscriptionsPlans : builder.query<tSubscriptionsPlansResponse[], void>({
      query: () => ({
        url: `/subscriptions/plans`,
        method: "GET",
      }),
    }),

    subscribeToPlan: builder.mutation<void, tUserToPlanSubscriptionRequest>({
      query: ({ user_id, plan_id }) => ({
        url: `/subscriptions/subscribe`,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id, plan_id }),
      }),
    }),

    checkIfUserIsFree: builder.query<boolean, string>({
      query: (userId) => ({
        url: `/subscriptions/is_free/${userId}`,
        method: "GET",
      }),
    }),

    getUserSubscriptionPlan: builder.query<tUserSubscriptionPlanMetaDataResponse | null, string>({
      query: (userId) => ({
        url: `/subscriptions/plan/${userId}`,
        method: "GET",
      }),
    }),

    getUserFavouriteMovies: builder.query<tMovieResponse[], string>({
      query: (userId) => `/movies/fav/${userId}`,
    }),

    addMovieToFavourites: builder.mutation<void, tFavMovieRequest>({
      query: (body) => ({
        url: `/movies/fav/add`,
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body,
      }),
    }),
    removeMovieFromFavourites: builder.mutation<void, tFavMovieRequest>({
      query: (body) => ({
        url: `/movies/fav/remove`,
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body,
      }),
    }),

    checkIfMovieIsFavourite: builder.mutation<{ is_favorite: boolean }, tFavMovieRequest>({
      query: (body) => ({
        url: "/movies/fav/check",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body,
      }),
    }),
  }),
});

export const {  useRegisterUserMutation, 
                useLoginUserMutation,
                useGetMoviesQuery, 
                useGetMovieDetailsQuery,
                useUpdateUserProfileMutation,
                useSearchMoviesQuery,
                useGetSubscriptionsPlansQuery,
                useSubscribeToPlanMutation,
                useCheckIfUserIsFreeQuery,
                useGetUserSubscriptionPlanQuery,
                useGetUserFavouriteMoviesQuery,
                useAddMovieToFavouritesMutation,
                useRemoveMovieFromFavouritesMutation,
                useCheckIfMovieIsFavouriteMutation,
        } = authApi;
