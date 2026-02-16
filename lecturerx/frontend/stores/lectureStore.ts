import { create } from "zustand";

import { api } from "@/lib/api";
import { Lecture } from "@/lib/types";

interface LectureStore {
  lectures: Lecture[];
  currentLecture: Lecture | null;
  isUploading: boolean;
  isProcessing: boolean;
  fetchLectures: () => Promise<void>;
  fetchLecture: (id: string) => Promise<void>;
  uploadLecture: (params: { title: string; file: File }) => Promise<Lecture>;
  deleteLecture: (id: string) => Promise<void>;
}

export const useLectureStore = create<LectureStore>((set, get) => ({
  lectures: [],
  currentLecture: null,
  isUploading: false,
  isProcessing: false,

  async fetchLectures() {
    const lectures = await api.listLectures();
    set({ lectures });
  },

  async fetchLecture(id: string) {
    const lecture = await api.getLecture(id);
    set({ currentLecture: lecture, isProcessing: lecture.processing_status !== "complete" });
  },

  async uploadLecture({ title, file }) {
    set({ isUploading: true });
    try {
      const extension = file.name.split(".").pop()?.toLowerCase() ?? "pdf";
      const { upload_url } = await api.getPresignedUploadUrl(file.name, file.type);
      const uploadResponse = await fetch(upload_url, {
        method: "PUT",
        headers: {
          "Content-Type": file.type
        },
        body: file
      });

      if (!uploadResponse.ok) {
        throw new Error("Failed to upload file to storage.");
      }

      const lecture = await api.createLecture({
        title,
        file_url: upload_url.split("?")[0],
        file_type: extension,
        file_size_bytes: file.size
      });

      set({ lectures: [lecture, ...get().lectures], currentLecture: lecture, isProcessing: true });
      return lecture;
    } finally {
      set({ isUploading: false });
    }
  },

  async deleteLecture(id: string) {
    await api.deleteLecture(id);
    set({
      lectures: get().lectures.filter((lecture) => lecture.id !== id),
      currentLecture: get().currentLecture?.id === id ? null : get().currentLecture
    });
  }
}));
