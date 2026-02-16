import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";

import "./globals.css";
import { ApiAuthBridge } from "@/components/layout/ApiAuthBridge";

export const metadata: Metadata = {
  title: "LectureRx",
  description: "AI-powered lecture processing for medical students"
};

export default function RootLayout({ children }: { children: React.ReactNode }): JSX.Element {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <ApiAuthBridge />
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
