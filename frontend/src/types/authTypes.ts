import { z } from 'zod';
import type {
  authResponseSchema,
  entityResponseSchema,
  favMovieRequestSchema,
  loginRequestSchema,
  movieDetailsResponseSchema,
  movieRequestSchema,
  registerFormSchema,
  registerRequestSchema,
  rootStateSchema,
  searchMovieResponseSchema,
  subscriptionsPlansResponseSchema,
  userProfileUpdateSchema,
  userSchema,
  userSubscriptionPlanMetaDataResponseSchema,
  userToPlanSubscriptionRequestSchema,
} from '../schemas/authSchemas';

export type tLoginRequest = z.infer<typeof loginRequestSchema>;
export type tRegisterRequest = z.infer<typeof registerRequestSchema>;
export type tRegisterForm = z.infer<typeof registerFormSchema>;
export type tAuthResponse = z.infer<typeof authResponseSchema>;
export type tRootState = z.infer<typeof rootStateSchema>;
export type tMovieResponse = z.infer<typeof movieRequestSchema>;
export type tMovieDetailsResponse = z.infer<typeof movieDetailsResponseSchema>;
export type tUpdateUserDataResponse = z.infer<typeof userProfileUpdateSchema>;
export type tSearchMoviesResponse = z.infer<typeof searchMovieResponseSchema>;
export type tSubscriptionsPlansResponse = z.infer<typeof subscriptionsPlansResponseSchema>;
export type tUserSubscriptionPlanMetaDataResponse = z.infer<
  typeof userSubscriptionPlanMetaDataResponseSchema
>;
export type tUserToPlanSubscriptionRequest = z.infer<typeof userToPlanSubscriptionRequestSchema>;
export type tFavMovieRequest = z.infer<typeof favMovieRequestSchema>;
export type tEntityResponse = z.infer<typeof entityResponseSchema>;

export type tUser = z.infer<typeof userSchema>;
export type tUserListResponse = tUser[];

export type tAddMovieRequest = {
  movie_name: string;
  movie_rating: number;
  movie_release_date: string;
  movie_pg: string;
  movie_description: string;

  actor_ids: string;
  director_ids: string;
  genre_ids: string;

  movie_poster: string;
  movie_preview_poster: string;

  movie_trailer: string;
  movie_language: string;

  movie_subtitles_language: string;
  movie_subtitles: object;

  license_id: string;
};

export type tSearchEntityResponse = {
  id: string;
  name: string;
};
