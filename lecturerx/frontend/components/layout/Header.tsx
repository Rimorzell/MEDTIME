"use client";

import { UserButton } from "@clerk/nextjs";

export function Header(): JSX.Element {
  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
      <h1 className="text-lg font-semibold text-slate-900">LectureRx Dashboard</h1>
      <UserButton afterSignOutUrl="/" />
    </header>
  );
}
