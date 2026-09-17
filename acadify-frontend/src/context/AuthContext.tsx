import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import type { User } from "../types";

interface AuthContextType {
  user: User | null;

  accessToken: string | null;

  isAuthenticated: boolean;

  isLoading: boolean;

  login: (
    token: string,
    user: User
  ) => void;

  logout: () => void;
}

const AuthContext =
  createContext<
    AuthContextType | undefined
  >(undefined);

export function AuthProvider({
  children,
}: {
  children: ReactNode;
}) {

  const [user, setUser] =
    useState<User | null>(null);

  const [accessToken, setAccessToken] =
    useState<string | null>(null);

  const [isLoading, setIsLoading] =
    useState(true);

  useEffect(() => {

    const token =
      localStorage.getItem(
        "access_token"
      );

    const storedUser =
      localStorage.getItem("user");

    if (token && storedUser) {

      try {

        const parsedUser =
          JSON.parse(storedUser);

        setAccessToken(token);
        setUser(parsedUser);

      } catch (error) {

        console.error(
          "Failed to restore authentication:",
          error
        );

        localStorage.removeItem(
          "access_token"
        );

        localStorage.removeItem(
          "user"
        );
      }
    }

    setIsLoading(false);

  }, []);

  const login = (
    token: string,
    userData: User
  ) => {

    localStorage.setItem(
      "access_token",
      token
    );

    localStorage.setItem(
      "user",
      JSON.stringify(userData)
    );

    setAccessToken(token);
    setUser(userData);
  };

  const logout = () => {

    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "user"
    );

    setAccessToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        accessToken,
        isAuthenticated:
          !!accessToken,
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {

  const context =
    useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider"
    );
  }

  return context;
}