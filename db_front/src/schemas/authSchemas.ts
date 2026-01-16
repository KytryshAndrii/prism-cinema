import { z } from "zod";

export const loginRequestSchema = z.object({
  login: z.string().min(3),
  password: z.string().min(6),
});

export const registerFormSchema = loginRequestSchema.extend({
  email: z.string(),
  dateOfBirth: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
});

export const registerRequestSchema = registerFormSchema.extend({
  region: z.string(),
})

export const authResponseSchema = z.object({
  id: z.string(),
  login: z.string(),
  email: z.string(),
  region: z.string(),
  birthday: z.string(),
  isUserSubscribed: z.boolean(),
  isUserAdmin: z.boolean(),
  token: z.string(),
});

export const userProfileUpdateSchema = z.object({
  email: z.string().optional(),
  userId: z.string().optional(),
  login: z.string().optional(),
  password: z.string().optional(),
})

export const rootStateSchema = z.object({
  user: authResponseSchema,
});

export const movieRequestSchema = z.object({
  movie_id: z.string(),
  movie_name: z.string(),
  movie_poster: z.string(),
});

export const movieDetailsResponseSchema = z.object({
  description: z.string(),
  trailer_url: z.string(),
  pg: z.string(),
  rating: z.string(),
  release_date: z.string(),
  genres: z.array(z.string()),
  actors: z.array(z.string()),
  directors: z.array(z.string()),
  movie_preview_poster: z.string(),
  movie_poster: z.string(),
});

const searchMovieResponse = z.object({ 
  id: z.string(),
  name: z.string()
});

export const searchMovieResponseSchema = z.array(searchMovieResponse);

export const subscriptionsPlansResponseSchema = z.object({
  id: z.string(),
  sub_type:z.string(),
  sub_cost:z.string(),
  sub_description:z.string()
})

export const userSubscriptionPlanMetaDataResponseSchema = z.object({ 
  id: z.string(), 
  sub_type: z.string() 
})

export const userToPlanSubscriptionRequestSchema = z.object({
    user_id: z.string(), 
    plan_id: z.string() 
})

export const favMovieRequestSchema = z.object({
  user_id: z.string(),
  movie_id: z.string(),
});

export const movieEnitySchema = z.object({
  movie_id: z.string(),
  movie_name: z.string(),
})

export const entityResponseSchema = z.object({
  id: z.string(),
  name: z.string(),
  birthplace: z.string().optional(),
  description: z.string().optional(),
  movies: movieEnitySchema.array(),
})
