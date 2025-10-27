"use client";
import { useState } from "react";
import { bffFetch, bffUrl } from "@/lib/api";

type Status = "idle" | "pending" | "completed" | "failed";

export function useExportReport(reportSlug: string) {
  const [status, setStatus] = useState<Status>("idle");
  const [taskId, setTaskId] = useState<string | null>(null);
  const [filename, setFilename] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const startExport = async (format: "pdf" | "csv") => {
    setStatus("pending"); setError(null); setFilename(null); setTaskId(null);
    const res = await bffFetch(`/api/export/${reportSlug}?format=${format}`, { method: "POST" });
    if (!res.ok) { setStatus("failed"); setError(await res.text()); return; }
    const j = await res.json(); setTaskId(j.task_id); pollStatus(j.task_id);
  };

  const pollStatus = async (tid: string) => {
    const t = setInterval(async () => {
      const r = await bffFetch(`/api/export/status/${tid}`);
      const j = await r.json();
      if (j.status === "completed" && j.result?.filename) { setStatus("completed"); setFilename(j.result.filename); clearInterval(t); }
      if (j.status === "failed") { setStatus("failed"); setError(j.error || "Export failed"); clearInterval(t); }
    }, 1500);
  };

  const download = () => {
    if (!filename) return;
    const link = document.createElement("a");
    link.href = bffUrl(`/api/export/download/${filename}`);
    link.download = filename;
    link.rel = "noopener";
    link.target = "_blank";
    document.body.appendChild(link); link.click(); link.remove();
  };

  return { status, taskId, filename, error, startExport, download };
}
