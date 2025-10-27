"use client";
import { useState, useRef, useEffect } from "react";
import { useExportReport } from "@/hooks/useExportReport";

type Props = { reportSlug: string };

export default function ExportDropdown({ reportSlug }: Props) {
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const { status, filename, error, startExport, download } = useExportReport(reportSlug);

  useEffect(() => {
    const onClick = (e: MouseEvent) => { if (menuRef.current && !menuRef.current.contains(e.target as Node)) setOpen(false); };
    window.addEventListener("click", onClick); return () => window.removeEventListener("click", onClick);
  }, []);

  return (
    <div className="relative" ref={menuRef}>
      <button onClick={() => setOpen((o) => !o)} className="inline-flex items-center gap-2 rounded-xl px-4 py-2 bg-emerald-600 text-white shadow-sm hover:bg-emerald-700 transition">
        Export
        <svg className={`h-4 w-4 transition-transform ${open ? "rotate-180" : ""}`} viewBox="0 0 20 20" fill="currentColor">
          <path d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 011.06 1.06l-4.24 4.25a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" />
        </svg>
      </button>
      <div className={`absolute right-0 mt-2 w-36 rounded-xl border border-gray-200 bg-white shadow-xl transition-all duration-150 ${open ? "opacity-100 translate-y-0" : "pointer-events-none opacity-0 -translate-y-1"}`}>
        {(["pdf","csv"] as const).map((fmt) => (
          <button key={fmt} onClick={() => { setOpen(false); startExport(fmt); }} className="w-full text-left px-4 py-2 text-sm hover:bg-gray-50 capitalize">{fmt}</button>
        ))}
      </div>
      <div className="mt-2 min-h-[1.5rem]">
        {status === "pending" && <p className="text-sm text-gray-500 animate-pulse">Generating…</p>}
        {status === "completed" && filename && (<button onClick={download} className="text-sm text-blue-600 hover:underline">Download {filename}</button>)}
        {status === "failed" && <p className="text-sm text-red-600">Export failed{error ? `: ${error}` : ""}</p>}
      </div>
    </div>
  );
}
