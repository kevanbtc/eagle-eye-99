// Hooks - useApi

import { useAuth } from "./useAuth";
import axios, { AxiosInstance, AxiosError } from "axios";
import { useCallback } from "react";

interface UseApiReturn {
  get: <T = any>(url: string, config?: any) => Promise<any>;
  post: <T = any>(url: string, data?: any, config?: any) => Promise<any>;
  put: <T = any>(url: string, data?: any, config?: any) => Promise<any>;
  delete: <T = any>(url: string, config?: any) => Promise<any>;
  upload: (url: string, file: File) => Promise<any>;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const useApi = (): UseApiReturn => {
  const { token, logout } = useAuth();

  // Create axios instance
  const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
  });

  // Add authorization header
  if (token?.access_token) {
    axiosInstance.defaults.headers.common["Authorization"] =
      `Bearer ${token.access_token}`;
  }

  // Handle errors
  axiosInstance.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
      if (error.response?.status === 401) {
        // Token expired or invalid
        logout();
        window.location.href = "/login";
      }
      return Promise.reject(error);
    }
  );

  const get = useCallback(
    async <T = any>(url: string, config?: any) => {
      try {
        const response = await axiosInstance.get<T>(url, config);
        return response.data;
      } catch (error) {
        console.error("GET error:", error);
        throw error;
      }
    },
    [axiosInstance]
  );

  const post = useCallback(
    async <T = any>(url: string, data?: any, config?: any) => {
      try {
        const response = await axiosInstance.post<T>(url, data, config);
        return response.data;
      } catch (error) {
        console.error("POST error:", error);
        throw error;
      }
    },
    [axiosInstance]
  );

  const put = useCallback(
    async <T = any>(url: string, data?: any, config?: any) => {
      try {
        const response = await axiosInstance.put<T>(url, data, config);
        return response.data;
      } catch (error) {
        console.error("PUT error:", error);
        throw error;
      }
    },
    [axiosInstance]
  );

  const del = useCallback(
    async <T = any>(url: string, config?: any) => {
      try {
        const response = await axiosInstance.delete<T>(url, config);
        return response.data;
      } catch (error) {
        console.error("DELETE error:", error);
        throw error;
      }
    },
    [axiosInstance]
  );

  const upload = useCallback(
    async (url: string, file: File) => {
      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await axiosInstance.post(url, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        return response.data;
      } catch (error) {
        console.error("Upload error:", error);
        throw error;
      }
    },
    [axiosInstance]
  );

  return {
    get,
    post,
    put,
    delete: del,
    upload,
  };
};
