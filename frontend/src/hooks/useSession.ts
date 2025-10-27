"use client";
import { useState, useEffect, useCallback } from "react";
import { bffFetch } from "@/lib/api";

export type SessionUser = { sub?: string; role?: "admin"|"engineer"|"manager"|"operator" };

export function useSession() {
  const [user, setUser] = useState<SessionUser | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchSession = useCallback(async () => {
    setLoading(true);
    try {
      const res = await bffFetch("/api/auth/me");
      const data = await res.json();
      setUser(data?.authenticated ? data.user : null);
    } finally {
      setLoading(false);
    }
  }, []);

  const login = async (username: string, password: string) => {
    const res = await bffFetch("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) throw new Error(await res.text());
    await fetchSession();
  };

  const logout = async () => {
    await bffFetch("/api/auth/logout", { method: "POST" });
    setUser(null);
  };

  useEffect(() => { fetchSession(); }, [fetchSession]);
  return { user, loading, login, logout, refresh: fetchSession };
}
