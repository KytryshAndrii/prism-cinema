import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import type {
  tAddMovieRequest,
  tAuthResponse,
  tEntityResponse,
  tFavMovieRequest,
  tLoginRequest,
  tMovieDetailsResponse,
  tMovieResponse,
  tRegisterRequest,
  tRootState,
  tSearchEntityResponse,
  tSubscriptionsPlansResponse,
  tUpdateUserDataResponse,
  tUserListResponse,
  tUserSubscriptionPlanMetaDataResponse,
  tUserToPlanSubscriptionRequest,
} from '../types/authTypes';

export const authApi = createApi({
  reducerPath: 'authApi',
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_PRISM_CINEMA_BACKEND,
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as tRootState).user.token;
      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Users', 'Movies'],


  endpoints: builder => ({
    registerUser: builder.mutation<tAuthResponse, tRegisterRequest>({
      query: body => ({
        url: '/register',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }),
    }),

    loginUser: builder.mutation<tAuthResponse, tLoginRequest>({
      query: body => ({
        url: '/login',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }),
    }),

    updateUserProfile: builder.mutation<void, tUpdateUserDataResponse>({
      query: ({ userId, ...body }) => ({
        url: `/update/user/${userId}`,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }),
    }),

    searchMovies: builder.query<tMovieResponse[], string>({
      query: query => ({
        url: `/search/movies?query=${encodeURIComponent(query)}`,
        method: 'GET',
      }),
       transformResponse: (response: { id: string; name: string }[]) =>
        response.map(movie => ({
        movie_id: movie.id,
        movie_name: movie.name,
        movie_poster: '', 
    })),
      providesTags: ['Movies'],
    }),

    getMovies: builder.query<tMovieResponse[], void>({
      query: () => ({
        url: '/movies',
        method: 'GET',
      }),
      providesTags: ['Movies'],
    }),

    getMovieDetails: builder.query<tMovieDetailsResponse, string>({
      query: movieId => ({
        url: `/movie_details/${movieId}`,
        method: 'GET',
      }),
    }),

    getSubscriptionsPlans: builder.query<tSubscriptionsPlansResponse[], void>({
      query: () => ({
        url: `/subscriptions/plans`,
        method: 'GET',
      }),
    }),

    subscribeToPlan: builder.mutation<void, tUserToPlanSubscriptionRequest>({
      query: ({ user_id, plan_id }) => ({
        url: `/subscriptions/subscribe`,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id, plan_id }),
      }),
    }),

    checkIfUserIsFree: builder.query<boolean, string>({
      query: userId => ({
        url: `/subscriptions/is_free/${userId}`,
        method: 'GET',
      }),
    }),

    getUserSubscriptionPlan: builder.query<tUserSubscriptionPlanMetaDataResponse | null, string>({
      query: userId => ({
        url: `/subscriptions/plan/${userId}`,
        method: 'GET',
      }),
    }),

    getUserFavouriteMovies: builder.query<tMovieResponse[], string>({
      query: userId => `/movies/fav/${userId}`,
    }),

    addMovieToFavourites: builder.mutation<void, tFavMovieRequest>({
      query: body => ({
        url: `/movies/fav/add`,
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
      }),
    }),
    removeMovieFromFavourites: builder.mutation<void, tFavMovieRequest>({
      query: body => ({
        url: `/movies/fav/remove`,
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
      }),
    }),

    checkIfMovieIsFavourite: builder.mutation<{ is_favorite: boolean }, tFavMovieRequest>({
      query: body => ({
        url: '/movies/fav/check',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body,
      }),
    }),

    getActorEntity: builder.query<tEntityResponse, string>({
      query: name => `/entity/actor/${encodeURIComponent(name)}`,
    }),

    getDirectorEntity: builder.query<tEntityResponse, string>({
      query: name => `/entity/director/${encodeURIComponent(name)}`,
    }),

    getGenreEntity: builder.query<tEntityResponse, string>({
      query: name => `/entity/genre/${encodeURIComponent(name)}`,
    }),

    getUsers: builder.query<tUserListResponse, void>({
      query: () =>({
        url: `/users`,
        method: 'GET',
        
      }),
      providesTags: ['Users'],
    }),
    
    deleteUser: builder.mutation<{ success: boolean }, string>({
      query: userId => ({
        url: `/delete/user/${userId}`,
        method: 'DELETE',
      }),
       invalidatesTags: ['Users'],
    }),
    
    searchUsers: builder.query<tUserListResponse, string>({
      query: phrase => `/search/users?query=${encodeURIComponent(phrase)}`,
      providesTags: ['Users'],
    }),

    deleteMovie: builder.mutation<void, string>({
      query: movieId => ({
      url: `/delete/movie/${movieId}`,
      method: 'DELETE',
      }),
      invalidatesTags: ['Movies'],
    }),

    addMovie: builder.mutation<{ movie_id: string }, tAddMovieRequest>({
      query: body => ({
        url: '/add/movies',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body,
      }),
      invalidatesTags: ['Movies'],
    }),

    searchActors: builder.query<tSearchEntityResponse[], string>({
      query: phrase => `/search/actors?query=${encodeURIComponent(phrase)}`,
    }),

    searchDirectors: builder.query<tSearchEntityResponse[], string>({
      query: phrase => `/search/directors?query=${encodeURIComponent(phrase)}`,
    }),

    searchGenres: builder.query<tSearchEntityResponse[], string>({
      query: phrase => `/search/genres?query=${encodeURIComponent(phrase)}`,
    }),
  }),
});

export const {
  useRegisterUserMutation,
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
  useGetActorEntityQuery,
  useGetDirectorEntityQuery,
  useGetGenreEntityQuery,
  useGetUsersQuery,
  useDeleteUserMutation,
  useSearchUsersQuery,
  useDeleteMovieMutation,
  useAddMovieMutation,
  useSearchActorsQuery,
  useSearchDirectorsQuery,
  useSearchGenresQuery,
} = authApi;
