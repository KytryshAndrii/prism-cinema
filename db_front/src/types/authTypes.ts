import { z } from "zod";
import type { authResponseSchema, favMovieRequestSchema, loginRequestSchema, movieDetailsResponseSchema, movieRequestSchema, registerFormSchema, registerRequestSchema, rootStateSchema, searchMovieResponseSchema, subscriptionsPlansResponseSchema, userProfileUpdateSchema, userSubscriptionPlanMetaDataResponseSchema, userToPlanSubscriptionRequestSchema } from "../schemas/authSchemas";

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
export type tUserSubscriptionPlanMetaDataResponse = z.infer<typeof userSubscriptionPlanMetaDataResponseSchema>;
export type tUserToPlanSubscriptionRequest = z.infer<typeof userToPlanSubscriptionRequestSchema>
export type tFavMovieRequest = z.infer<typeof favMovieRequestSchema>;