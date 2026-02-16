"use client";

import { useAuth, useUser } from "@clerk/nextjs";
import { useEffect } from "react";

import { configureApiAuth } from "@/lib/api";

export function ApiAuthBridge(): null {
  const { getToken } = useAuth();
  const { user } = useUser();

  useEffect(() => {
    configureApiAuth({
      getToken: () => getToken(),
      getUserMeta: () => ({ clerkId: user?.id ?? null, email: user?.primaryEmailAddress?.emailAddress ?? null })
    });
  }, [getToken, user?.id, user?.primaryEmailAddress?.emailAddress]);

  return null;
}
