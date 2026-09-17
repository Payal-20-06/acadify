export type UserRole = "student" | "teacher" | "admin";

export interface User {
  uid: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  is_verified: boolean;
}

export interface AuthTokens {
  access_token: string;
  refresh_token?: string;
  token_type: string;
}