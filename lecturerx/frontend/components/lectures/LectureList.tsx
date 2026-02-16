import { Lecture } from "@/lib/types";

import { LectureCard } from "./LectureCard";

interface LectureListProps {
  lectures: Lecture[];
}

export function LectureList({ lectures }: LectureListProps): JSX.Element {
  if (lectures.length === 0) {
    return <p className="text-sm text-slate-500">No lectures yet. Upload your first lecture to get started.</p>;
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {lectures.map((lecture) => (
        <LectureCard key={lecture.id} lecture={lecture} />
      ))}
    </div>
  );
}
