"use client";
import ExportDropdown from "@/components/ExportDropdown";
import { useSession } from "@/hooks/useSession";

export default function ReportPage({ params }: { params: { report: string } }) {
  const { user, loading } = useSession();
  if (loading) return <p className="p-6 text-gray-500">Loading…</p>;
  if (!user) return <p className="p-6 text-red-600">Please log in.</p>;
  const title = params.report.replace(/-/g, " ");
  return (
    <section className="p-6">
      <header className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold capitalize">{title}</h1>
        <ExportDropdown reportSlug={params.report} />
      </header>
      <p className="text-gray-500">Report content placeholder for {title}</p>
    </section>
  );
}
