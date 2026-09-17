import api from "./api";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  full_name: string;
  email: string;
  phone: string;
  role: "student" | "teacher";
  password: string;
  confirm_password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
}

const authService = {

  async login(data: LoginPayload) {
    const response =
      await api.post<LoginResponse>(
        "/api/v1/auths/login",
        data
      );

    return response.data;
  },

  async register(
    data: RegisterPayload
  ) {
    const response =
      await api.post(
        "/api/v1/auths/signup",
        data
      );

    return response.data;
  },

  async getCurrentUser() {
    const response =
      await api.get(
        "/api/v1/users/me"
      );

    return response.data;
  },

};

export default authService;