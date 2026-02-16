import Link from "next/link";

import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Lecture } from "@/lib/types";

interface LectureCardProps {
  lecture: Lecture;
}

export function LectureCard({ lecture }: LectureCardProps): JSX.Element {
  const isComplete = lecture.processing_status === "complete";

  return (
    <Link href={`/lectures/${lecture.id}`}>
      <Card className="space-y-3 hover:border-blue-400">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-slate-900">{lecture.title}</h3>
          <Badge tone={isComplete ? "success" : "default"}>{isComplete ? "✅ complete" : "processing"}</Badge>
        </div>
        <p className="text-xs text-slate-500">{new Date(lecture.created_at).toLocaleDateString()}</p>
        <div className="grid grid-cols-3 gap-2 text-xs text-slate-600">
          <span>Concepts: {lecture.concept_count}</span>
          <span>Cards: {lecture.flashcard_count}</span>
          <span>Questions: {lecture.question_count}</span>
        </div>
      </Card>
    </Link>
  );
}
