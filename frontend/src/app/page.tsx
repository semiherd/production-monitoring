"use client";
import { useSession } from "@/hooks/useSession";
export default function Home() {
  const { user, loading, login, logout } = useSession();
  if (loading) return <main className="p-6">Loading…</main>;
  return (
    <main className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">SmartLine Dashboard</h1>
      {user ? (
        <div className="space-x-3">
          <span className="text-gray-600">Hello, {user.sub || "user"} ({user.role})</span>
          <a className="text-blue-600 underline" href="/reports/daily-production">Go to Daily Production</a>
          <button className="px-3 py-1 bg-gray-200 rounded" onClick={logout}>Logout</button>
        </div>
      ) : (
        <form className="space-x-2" onSubmit={async (e) => { e.preventDefault(); const f = new FormData(e.currentTarget as HTMLFormElement); await login(String(f.get("u")), String(f.get("p"))); }}>
          <input name="u" placeholder="username" className="border rounded px-2 py-1" />
          <input name="p" type="password" placeholder="password" className="border rounded px-2 py-1" />
          <button className="px-3 py-1 bg-emerald-600 text-white rounded">Login</button>
        </form>
      )}
    </main>
  );
}
