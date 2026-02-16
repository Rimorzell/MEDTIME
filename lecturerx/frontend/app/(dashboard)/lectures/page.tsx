"use client";

import { useEffect } from "react";

import { LectureList } from "@/components/lectures/LectureList";
import { useLectureStore } from "@/stores/lectureStore";

export default function LecturesPage(): JSX.Element {
  const lectures = useLectureStore((state) => state.lectures);
  const fetchLectures = useLectureStore((state) => state.fetchLectures);

  useEffect(() => {
    void fetchLectures();
  }, [fetchLectures]);

  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-semibold text-slate-900">My Lectures</h2>
      <LectureList lectures={lectures} />
    </section>
  );
}
