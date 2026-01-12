import { z } from "zod";

export const loginRequestSchema = z.object({
  login: z
    .string()
    .min(3, "Login must contain minimum 3 signs.")
    .nonempty("Login cannot be empty."),
  password: z
    .string()
    .min(6, "Password must contain minimum 6 signs.")
    .nonempty("Password cannot be empty."),
});

export const registerRequestSchema = loginRequestSchema.extend({
  email: z
    .string()
    .nonempty("Email cannot be empty.")
    .refine((val) => val.includes("@") && val.includes("."), {
      message: "Email must contain '@' and '.'",
    }),
  dateOfBirth: z
    .string()
    .nonempty("Date of birth cannot be empty.")
    .regex(/^\d{4}-\d{2}-\d{2}$/, "Date must be in format YYYY-MM-DD"),
});
