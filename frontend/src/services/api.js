// Small API helper using fetch. This satisfies the requirement to consume Flask data.
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

export function getToken() {
  return localStorage.getItem("token");
}

export async function apiRequest(path, options = {}) {
  const token = getToken();

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || data.message || "Something went wrong.");
  }

  return data;
}

export default API_URL;
