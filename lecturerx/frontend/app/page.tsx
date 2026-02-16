import Link from "next/link";

import { Button } from "@/components/ui/button";

export default function LandingPage(): JSX.Element {
  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col items-center justify-center px-6 text-center">
      <h1 className="text-5xl font-bold text-slate-900">LectureRx</h1>
      <p className="mt-4 max-w-xl text-slate-600">
        Transform lecture slides into board-focused concepts, flashcards, and practice questions.
      </p>
      <div className="mt-8 flex gap-4">
        <Link href="/sign-in">
          <Button>Sign In</Button>
        </Link>
        <Link href="/sign-up">
          <Button variant="outline">Create Account</Button>
        </Link>
      </div>
    </main>
  );
}
