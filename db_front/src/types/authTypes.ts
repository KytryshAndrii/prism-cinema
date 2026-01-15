import { z } from "zod";
import type { authResponseSchema, loginRequestSchema, movieDetailsResponseSchema, movieRequestSchema, registerRequestSchema, rootStateSchema, userProfileUpdateSchema } from "../schemas/authSchemas";

export type tLoginRequest = z.infer<typeof loginRequestSchema>;
export type tRegisterRequest = z.infer<typeof registerRequestSchema>;
export type tAuthResponse = z.infer<typeof authResponseSchema>;
export type tRootState = z.infer<typeof rootStateSchema>;
export type tMovieResponse = z.infer<typeof movieRequestSchema>;
export type tMovieDetailsResponse = z.infer<typeof movieDetailsResponseSchema>;
export type tUpdateUserDataResponse = z.infer<typeof userProfileUpdateSchema>;