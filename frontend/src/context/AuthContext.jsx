// AuthContext keeps user login state available across the app.
import { createContext, useContext, useEffect, useState } from "react";
import { apiRequest } from "../services/api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // useEffect checks if a saved token exists when the page refreshes.
  useEffect(() => {
    async function loadUser() {
      const token = localStorage.getItem("token");
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const profile = await apiRequest("/auth/me");
        setUser(profile);
      } catch (error) {
        localStorage.removeItem("token");
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, []);

  async function login(email, password) {
    const data = await apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    localStorage.setItem("token", data.token);
    setUser(data.user);
    return data.user;
  }

  async function register(username, email, password) {
    const data = await apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, email, password }),
    });
    localStorage.setItem("token", data.token);
    setUser(data.user);
    return data.user;
  }

  async function logout() {
    try {
      await apiRequest("/auth/logout", { method: "POST" });
    } catch (error) {
      // Even if the token has expired, remove it from the browser.
    }
    localStorage.removeItem("token");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
