import { useState } from "react";

import { RegisterForm } from "./RegisterForm";
import { LoginForm } from "./LoginForm";
import { Button } from "../../components/ui/button";
import { cn } from "../../lib/utils";

export default function Authentication() {
  const [isLogin, setIsLogin] = useState(true);
  return (
    <div className="container relative h-[100vh] flex-col items-center justify-center md:grid lg:max-w-none lg:grid-cols-2 lg:px-0">
      <Button
        variant="ghost"
        className={cn("absolute right-4 top-4 md:right-8 md:top-8")}
        onClick={() => {
          setIsLogin(!isLogin);
        }}
      >
        {isLogin ? "Register" : "Login"}
      </Button>
      <div className="relative lg:h-full flex-col bg-muted p-10 text-white dark:border-r lg:flex">
        <div className="absolute inset-0 bg-zinc-900" />
        <div className="relative z-20 flex items-center text-lg font-medium">
          Chatase
        </div>
        <div className="relative z-20 mt-auto">
          <blockquote className="space-y-2">
            <p className="text-lg">
              &ldquo;If you want your chatbot to have the most natural
              conversational experience the world has ever seen, then Chatase is
              the only choice.&rdquo;
            </p>
            <footer className="text-sm">Frank Wang - Chatase Creator</footer>
          </blockquote>
        </div>
      </div>
      <div className="lg:p-8">
        <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
          <div className="flex flex-col space-y-2 text-center">
            <h1 className="text-2xl font-semibold tracking-tight">
              {isLogin ? "Log in to an account" : "Create an account"}
            </h1>
            <p className="text-sm text-muted-foreground">
              Enter your email and password below to{" "}
              {isLogin ? "login to" : "create"} your account
            </p>
          </div>
          {isLogin ? <LoginForm /> : <RegisterForm />}

          {/* <p className="px-8 text-center text-sm text-muted-foreground">
            By clicking continue, you agree to our{" "}
            <Link
              href="/terms"
              className="underline underline-offset-4 hover:text-primary"
            >
              Terms of Service
            </Link>{" "}
            and{" "}
            <Link
              href="/privacy"
              className="underline underline-offset-4 hover:text-primary"
            >
              Privacy Policy
            </Link>
            .
          </p> */}
        </div>
      </div>
    </div>
  );
}
