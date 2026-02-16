"use client";

import { ChangeEvent, DragEvent, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useLectureStore } from "@/stores/lectureStore";

const allowedTypes = ["application/pdf", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "image/png", "image/jpeg"];

export function FileUploader(): JSX.Element {
  const router = useRouter();
  const uploadLecture = useLectureStore((state) => state.uploadLecture);
  const isUploading = useLectureStore((state) => state.isUploading);

  const [title, setTitle] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fileLabel = useMemo(() => {
    if (!file) return "No file selected";
    return `${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
  }, [file]);

  const selectFile = (incoming: File | null) => {
    if (!incoming) return;
    if (!allowedTypes.includes(incoming.type)) {
      setError("Unsupported file type. Use PDF, PPTX, PNG, or JPG.");
      return;
    }
    setError(null);
    setFile(incoming);
    if (!title) {
      setTitle(incoming.name.replace(/\.[^/.]+$/, ""));
    }
  };

  const onFileInput = (event: ChangeEvent<HTMLInputElement>) => selectFile(event.target.files?.[0] ?? null);

  const onDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    selectFile(event.dataTransfer.files?.[0] ?? null);
  };

  const onSubmit = async () => {
    if (!file || !title) {
      setError("Please provide a title and file.");
      return;
    }

    try {
      const lecture = await uploadLecture({ title, file });
      router.push(`/lectures/${lecture.id}`);
    } catch {
      setError("Upload failed. Please try again.");
    }
  };

  return (
    <div className="space-y-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <div
        onDrop={onDrop}
        onDragOver={(event) => event.preventDefault()}
        className="rounded-lg border border-dashed border-slate-300 p-8 text-center text-slate-500"
      >
        Drag and drop your lecture file here
        <div className="mt-3">
          <Input type="file" accept=".pdf,.pptx,.png,.jpg,.jpeg" onChange={onFileInput} />
        </div>
      </div>

      <div className="text-sm text-slate-600">{fileLabel}</div>
      <Input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Lecture Title" />

      {error ? <p className="text-sm text-red-600">{error}</p> : null}
      <Button onClick={onSubmit} disabled={isUploading}>
        {isUploading ? "Uploading..." : "Upload & Process"}
      </Button>
    </div>
  );
}
