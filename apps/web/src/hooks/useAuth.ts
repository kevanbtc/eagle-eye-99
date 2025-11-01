// Hooks - useAuth

import { useEffect, useState } from "react";
import { User, AuthToken } from "@/lib/types";

interface AuthState {
  user: User | null;
  token: AuthToken | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export const useAuth = () => {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
  });

  useEffect(() => {
    // Check if user is authenticated on mount
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const userStr = localStorage.getItem("user");

        if (token && userStr) {
          const user = JSON.parse(userStr);
          setState({
            user,
            token: JSON.parse(token),
            isAuthenticated: true,
            isLoading: false,
          });
        } else {
          setState((prev) => ({ ...prev, isLoading: false }));
        }
      } catch (error) {
        console.error("Auth check failed:", error);
        setState((prev) => ({ ...prev, isLoading: false }));
      }
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) throw new Error("Login failed");

      const data = await response.json();
      localStorage.setItem("access_token", JSON.stringify(data.token));
      localStorage.setItem("user", JSON.stringify(data.user));

      setState({
        user: data.user,
        token: data.token,
        isAuthenticated: true,
        isLoading: false,
      });

      return data;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
  };

  const register = async (email: string, password: string, firstName: string, lastName: string) => {
    try {
      const response = await fetch("/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, firstName, lastName }),
      });

      if (!response.ok) throw new Error("Registration failed");

      const data = await response.json();
      localStorage.setItem("access_token", JSON.stringify(data.token));
      localStorage.setItem("user", JSON.stringify(data.user));

      setState({
        user: data.user,
        token: data.token,
        isAuthenticated: true,
        isLoading: false,
      });

      return data;
    } catch (error) {
      console.error("Registration error:", error);
      throw error;
    }
  };

  return {
    ...state,
    login,
    logout,
    register,
  };
};
