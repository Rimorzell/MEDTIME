"use client";

import { useEffect } from "react";
import { useParams } from "next/navigation";

import { BoardMapTab } from "@/components/results/BoardMapTab";
import { FlashcardsTab } from "@/components/results/FlashcardsTab";
import { QuestionsTab } from "@/components/results/QuestionsTab";
import { SummaryTab } from "@/components/results/SummaryTab";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useLectureStore } from "@/stores/lectureStore";

export default function LectureDetailPage(): JSX.Element {
  const params = useParams<{ id: string }>();
  const currentLecture = useLectureStore((state) => state.currentLecture);
  const isProcessing = useLectureStore((state) => state.isProcessing);
  const fetchLecture = useLectureStore((state) => state.fetchLecture);

  useEffect(() => {
    void fetchLecture(params.id);
  }, [fetchLecture, params.id]);

  if (!currentLecture) {
    return <p className="text-sm text-slate-500">Loading lecture...</p>;
  }

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-slate-900">{currentLecture.title}</h2>
        <Badge tone={isProcessing ? "warning" : "success"}>{isProcessing ? "Processing..." : "Complete"}</Badge>
      </div>
      {isProcessing ? (
        <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4 text-sm text-yellow-800">
          Processing steps: parsing → extracting → mapping → generating
        </div>
      ) : null}
      <Tabs defaultValue="summary">
        <TabsList>
          <TabsTrigger value="summary">Summary</TabsTrigger>
          <TabsTrigger value="board-map">Board Map</TabsTrigger>
          <TabsTrigger value="flashcards">Flashcards</TabsTrigger>
          <TabsTrigger value="questions">Practice Questions</TabsTrigger>
        </TabsList>
        <TabsContent value="summary">
          <SummaryTab />
        </TabsContent>
        <TabsContent value="board-map">
          <BoardMapTab />
        </TabsContent>
        <TabsContent value="flashcards">
          <FlashcardsTab />
        </TabsContent>
        <TabsContent value="questions">
          <QuestionsTab />
        </TabsContent>
      </Tabs>
    </section>
  );
}
