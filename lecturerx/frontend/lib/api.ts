import axios, { AxiosInstance } from "axios";

import { Concept, Flashcard, Lecture, PracticeQuestion, QuestionAttempt } from "@/lib/types";

const apiBaseURL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

let getToken: (() => Promise<string | null>) | null = null;
let getUserMeta: (() => { clerkId: string | null; email: string | null }) | null = null;

export function configureApiAuth(options: {
  getToken: () => Promise<string | null>;
  getUserMeta: () => { clerkId: string | null; email: string | null };
}): void {
  getToken = options.getToken;
  getUserMeta = options.getUserMeta;
}

const client: AxiosInstance = axios.create({
  baseURL: apiBaseURL,
  timeout: 30000
});

client.interceptors.request.use(async (config) => {
  const token = getToken ? await getToken() : null;
  const meta = getUserMeta ? getUserMeta() : { clerkId: null, email: null };

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  if (meta.clerkId) {
    config.headers["x-clerk-user-id"] = meta.clerkId;
  }
  if (meta.email) {
    config.headers["x-user-email"] = meta.email;
  }

  return config;
});

export const api = {
  async getPresignedUploadUrl(file_name: string, file_type: string): Promise<{ upload_url: string }> {
    const { data } = await client.post("/api/uploads/presigned-url", { file_name, file_type });
    return data;
  },
  async createLecture(payload: {
    title: string;
    file_url: string;
    file_type: string;
    file_size_bytes?: number;
  }): Promise<Lecture> {
    const { data } = await client.post("/api/lectures", payload);
    return data;
  },
  async listLectures(): Promise<Lecture[]> {
    const { data } = await client.get("/api/lectures");
    return data;
  },
  async getLecture(id: string): Promise<Lecture> {
    const { data } = await client.get(`/api/lectures/${id}`);
    return data;
  },
  async deleteLecture(id: string): Promise<void> {
    await client.delete(`/api/lectures/${id}`);
  },
  async getConcepts(lectureId: string): Promise<Concept[]> {
    const { data } = await client.get(`/api/lectures/${lectureId}/concepts`);
    return data;
  },
  async getFlashcards(lectureId: string): Promise<Flashcard[]> {
    const { data } = await client.get(`/api/lectures/${lectureId}/flashcards`);
    return data;
  },
  async updateFlashcard(id: string, payload: Partial<Pick<Flashcard, "front_text" | "back_text" | "tags">>): Promise<Flashcard> {
    const { data } = await client.put(`/api/flashcards/${id}`, payload);
    return data;
  },
  async flagFlashcard(id: string): Promise<Flashcard> {
    const { data } = await client.post(`/api/flashcards/${id}/flag`);
    return data;
  },
  async exportFlashcards(lectureId: string): Promise<Blob> {
    const response = await client.get(`/api/lectures/${lectureId}/flashcards/export`, { responseType: "blob" });
    return response.data;
  },
  async getQuestions(lectureId: string): Promise<PracticeQuestion[]> {
    const { data } = await client.get(`/api/lectures/${lectureId}/questions`);
    return data;
  },
  async submitAttempt(
    id: string,
    payload: { selected_answer: string; time_spent_seconds?: number }
  ): Promise<QuestionAttempt> {
    const { data } = await client.post(`/api/questions/${id}/attempt`, payload);
    return data;
  }
};
