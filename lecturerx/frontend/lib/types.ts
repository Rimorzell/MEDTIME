export interface Lecture {
  id: string;
  user_id: string;
  title: string;
  file_url: string | null;
  file_type: string;
  file_size_bytes: number | null;
  organ_system: string | null;
  discipline: string | null;
  processing_status: string;
  processing_error: string | null;
  slide_count: number | null;
  concept_count: number;
  flashcard_count: number;
  question_count: number;
  created_at: string;
  updated_at: string;
}

export interface Concept {
  id: string;
  lecture_id: string;
  concept_name: string;
  definition: string | null;
  key_facts: string[] | null;
  discipline: string | null;
  organ_system: string | null;
  source_slide_numbers: number[] | null;
  board_relevance: "high" | "medium" | "school_only" | null;
  board_topic_id: string | null;
  board_topic_name: string | null;
  mapping_confidence: number | null;
  first_aid_chapter: number | null;
  first_aid_section: string | null;
  created_at: string;
}

export interface Flashcard {
  id: string;
  lecture_id: string;
  concept_id: string | null;
  front_text: string;
  back_text: string;
  card_type: "basic" | "cloze";
  tags: string[] | null;
  board_topic: string | null;
  source_slide_number: number | null;
  is_edited: boolean;
  is_flagged_incorrect: boolean;
  created_at: string;
}

export interface PracticeQuestion {
  id: string;
  lecture_id: string;
  concept_ids: string[] | null;
  question_stem: string;
  answer_choices: Array<{ letter: string; text: string }>;
  correct_answer: string;
  explanation: string;
  difficulty: "easy" | "medium" | "hard";
  created_at: string;
}

export interface QuestionAttempt {
  id: string;
  user_id: string;
  question_id: string;
  selected_answer: string;
  is_correct: boolean;
  time_spent_seconds: number | null;
  attempted_at: string;
}
