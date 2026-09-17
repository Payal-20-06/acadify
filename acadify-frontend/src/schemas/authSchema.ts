import { z } from "zod";

export const loginSchema = z.object({
  email: z
    .string()
    .min(1, "Email is required")
    .email("Enter a valid email address"),

  password: z
    .string()
    .min(1, "Password is required"),
});

export const registerSchema = z
  .object({
    full_name: z
      .string()
      .min(2, "Name must contain at least 2 characters"),

    email: z
      .string()
      .min(1, "Email is required")
      .email("Enter a valid email address"),

    phone: z
      .string()
      .min(10, "Enter a valid phone number"),

    role: z.enum(["student", "teacher"], {
      message: "Please select your role",
    }),

    password: z
      .string()
      .min(8, "Password must contain at least 8 characters"),

    confirm_password: z
      .string()
      .min(1, "Please confirm your password"),

    terms: z
      .boolean()
      .refine((value) => value === true, {
        message: "You must accept the terms",
      }),
  })
  .refine(
    (data) => data.password === data.confirm_password,
    {
      message: "Passwords do not match",
      path: ["confirm_password"],
    }
  );

export type LoginFormData = z.infer<typeof loginSchema>;

export type RegisterFormData =
  z.infer<typeof registerSchema>;