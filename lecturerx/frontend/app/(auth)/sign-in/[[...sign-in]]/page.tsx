import { SignIn } from "@clerk/nextjs";

export default function SignInPage(): JSX.Element {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <SignIn routing="path" path="/sign-in" signUpUrl="/sign-up" />
    </main>
  );
}
