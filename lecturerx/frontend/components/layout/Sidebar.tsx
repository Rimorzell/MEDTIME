"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";

const links = [
  { href: "/upload", label: "Upload" },
  { href: "/lectures", label: "My Lectures" }
];

export function Sidebar(): JSX.Element {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-slate-200 bg-white p-4">
      <div className="mb-8 text-xl font-semibold text-slate-900">LectureRx</div>
      <nav className="space-y-2">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={cn(
              "block rounded-md px-3 py-2 text-sm font-medium",
              pathname === link.href ? "bg-blue-600 text-white" : "text-slate-600 hover:bg-slate-100"
            )}
          >
            {link.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
