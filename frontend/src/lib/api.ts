export const BFF = process.env.NEXT_PUBLIC_BFF_BASE_URL || "";
export function bffUrl(path: string) {
  return `${BFF}${path.startsWith("/") ? path : `/${path}`}`;
}
export async function bffFetch(input: string, init: RequestInit = {}) {
  const url = bffUrl(input);
  const res = await fetch(url, {
    credentials: "include",
    ...init,
    headers: {
      ...(init.headers || {}),
      "Content-Type": (init.headers as any)?.["Content-Type"] ?? "application/json",
    },
  });
  return res;
}
