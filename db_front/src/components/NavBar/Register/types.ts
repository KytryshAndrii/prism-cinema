import type { z } from "zod";
import type { registerRequestSchema } from "../../../schemas/authSchemas";

export type tRegisterForm = z.infer<typeof registerRequestSchema>;