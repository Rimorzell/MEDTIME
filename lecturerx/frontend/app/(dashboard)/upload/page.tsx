import { FileUploader } from "@/components/upload/FileUploader";

export default function UploadPage(): JSX.Element {
  return (
    <section className="mx-auto max-w-3xl">
      <h2 className="mb-4 text-2xl font-semibold text-slate-900">Upload Lecture</h2>
      <FileUploader />
    </section>
  );
}
