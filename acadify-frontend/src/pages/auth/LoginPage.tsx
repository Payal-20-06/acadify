import {
  ArrowRight,
  Eye,
  EyeOff,
  GraduationCap,
  LockKeyhole,
  Mail,
} from "lucide-react";

import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import {
  loginSchema,
  type LoginFormData,
} from "../../schemas/authSchema";

import authService from "../../services/authService";
import { useAuth } from "../../context/AuthContext";

import studentImage from "../../assets/images/student.png";

function LoginPage() {
  const [showPassword, setShowPassword] =
    useState(false);

  const [rememberMe, setRememberMe] =
    useState(false);

  const navigate = useNavigate();

  const { login } = useAuth();

  const {
    register,
    handleSubmit,
    formState: {
      errors,
      isSubmitting,
    },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (
    data: LoginFormData
  ) => {
    try {
      console.log("Login data:", data);

      // 1. Login API
      const response =
        await authService.login(data);

      console.log(
        "Login response:",
        response
      );

      // 2. Save access token
      localStorage.setItem(
        "access_token",
        response.access_token
      );

      // 3. Get logged-in user
      const user =
        await authService.getCurrentUser();

      console.log(
        "Current user:",
        user
      );

      // 4. Save authentication state
      login(
        response.access_token,
        user
      );

      // 5. Redirect based on role
      if (user.role === "student") {
        navigate("/student/dashboard");
      } else if (
        user.role === "teacher"
      ) {
        navigate("/teacher/dashboard");
      } else if (
        user.role === "admin"
      ) {
        navigate("/admin/dashboard");
      } else {
        navigate("/");
      }

    } catch (error) {
      console.error(
        "Login failed:",
        error
      );
    }
  };

  return (
    <div className="min-h-screen bg-[#F2F6FC] px-4 py-8">

      <div className="mx-auto flex min-h-[calc(100vh-4rem)] max-w-6xl items-center justify-center">

        <div className="grid w-full overflow-hidden rounded-[32px] bg-white shadow-xl md:grid-cols-2">

          {/* ================= LEFT SIDE ================= */}

          <div className="relative hidden min-h-[650px] overflow-hidden bg-[#F2F6FC] md:flex">

            {/* Decorative circle */}

            <div className="absolute -left-16 -top-16 h-40 w-40 rounded-full bg-[#55C2C0]/20" />

            <div className="absolute bottom-10 left-10 h-24 w-24 rounded-full bg-[#F7C95C]/30" />

            <div className="absolute right-8 top-20 h-16 w-16 rounded-full bg-[#F58B35]/20" />

            <div className="relative z-10 flex w-full flex-col justify-between p-10">

              {/* Logo */}

              <Link
                to="/"
                className="flex items-center gap-2"
              >

                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#4662AD] text-white">
                  <GraduationCap size={22} />
                </div>

                <span className="heading-font text-2xl font-bold text-[#4662AD]">
                  Acadify
                </span>

              </Link>

              {/* Text */}

              <div className="mt-8">

                <p className="mb-3 text-xs font-bold tracking-[0.2em] text-[#55C2C0]">
                  WELCOME BACK
                </p>

                <h1 className="heading-font max-w-md text-4xl font-semibold leading-tight text-[#202536]">
                  Your academic journey continues here.
                </h1>

                <p className="mt-4 max-w-md text-sm leading-7 text-[#777B86]">
                  Log in to manage your subjects,
                  grades, attendance and assignments
                  from one simple platform.
                </p>

              </div>

              {/* Student Illustration */}

              <div className="flex flex-1 items-end justify-center">

                <img
                  src={studentImage}
                  alt="Acadify student"
                  className="max-h-[350px] object-contain"
                />

              </div>

            </div>
          </div>

          {/* ================= RIGHT SIDE ================= */}

          <div className="flex items-center justify-center px-6 py-10 sm:px-10 lg:px-14">

            <div className="w-full max-w-md">

              {/* Mobile Logo */}

              <div className="mb-8 flex items-center justify-center md:hidden">

                <Link
                  to="/"
                  className="flex items-center gap-2"
                >

                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#4662AD] text-white">
                    <GraduationCap size={22} />
                  </div>

                  <span className="heading-font text-2xl font-bold text-[#4662AD]">
                    Acadify
                  </span>

                </Link>

              </div>

              {/* Heading */}

              <div className="mb-8">

                <p className="mb-2 text-xs font-bold tracking-[0.2em] text-[#55C2C0]">
                  SIGN IN
                </p>

                <h2 className="heading-font text-3xl font-semibold text-[#202536]">
                  Welcome back
                </h2>

                <p className="mt-2 text-sm text-[#777B86]">
                  Sign in to continue to your Acadify account.
                </p>

              </div>

              {/* ================= FORM ================= */}

              <form
                onSubmit={handleSubmit(onSubmit)}
                className="space-y-5"
              >

                {/* Email */}

                <div>

                  <label className="mb-1.5 block text-sm font-medium text-[#202536]">
                    Email
                  </label>

                  <div className="relative">

                    <Mail
                      size={17}
                      className="absolute left-3 top-1/2 -translate-y-1/2 text-[#777B86]"
                    />

                    <input
                      type="email"
                      placeholder="Enter your email"
                      {...register("email")}
                      className="w-full rounded-xl border border-gray-200 bg-white py-3 pl-10 pr-4 text-sm outline-none transition focus:border-[#4662AD] focus:ring-2 focus:ring-[#4662AD]/10"
                    />

                  </div>

                  {errors.email && (
                    <p className="mt-1 text-xs text-red-500">
                      {errors.email.message}
                    </p>
                  )}

                </div>

                {/* Password */}

                <div>

                  <label className="mb-1.5 block text-sm font-medium text-[#202536]">
                    Password
                  </label>

                  <div className="relative">

                    <LockKeyhole
                      size={17}
                      className="absolute left-3 top-1/2 -translate-y-1/2 text-[#777B86]"
                    />

                    <input
                      type={
                        showPassword
                          ? "text"
                          : "password"
                      }
                      placeholder="Enter your password"
                      {...register("password")}
                      className="w-full rounded-xl border border-gray-200 bg-white py-3 pl-10 pr-11 text-sm outline-none transition focus:border-[#4662AD] focus:ring-2 focus:ring-[#4662AD]/10"
                    />

                    <button
                      type="button"
                      onClick={() =>
                        setShowPassword(
                          !showPassword
                        )
                      }
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-[#777B86] hover:text-[#4662AD]"
                    >
                      {showPassword ? (
                        <EyeOff size={17} />
                      ) : (
                        <Eye size={17} />
                      )}
                    </button>

                  </div>

                  {errors.password && (
                    <p className="mt-1 text-xs text-red-500">
                      {errors.password.message}
                    </p>
                  )}

                </div>

                {/* Remember + Forgot */}

                <div className="flex items-center justify-between">

                  <label className="flex cursor-pointer items-center gap-2">

                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(event) =>
                        setRememberMe(
                          event.target.checked
                        )
                      }
                      className="h-4 w-4 rounded border-gray-300 accent-[#4662AD]"
                    />

                    <span className="text-xs text-[#777B86]">
                      Remember me
                    </span>

                  </label>

                  <Link
                    to="/forgot-password"
                    className="text-xs font-semibold text-[#4662AD] hover:underline"
                  >
                    Forgot password?
                  </Link>

                </div>

                {/* Login Button */}

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-[#4662AD] py-3 text-sm font-semibold text-white transition hover:bg-[#3d579c] disabled:cursor-not-allowed disabled:opacity-60"
                >

                  {isSubmitting
                    ? "Signing in..."
                    : "Sign in"}

                  {!isSubmitting && (
                    <ArrowRight size={17} />
                  )}

                </button>

              </form>

              {/* Divider */}

              <div className="my-6 flex items-center gap-4">

                <div className="h-px flex-1 bg-gray-200" />

                <span className="text-xs text-[#777B86]">
                  OR
                </span>

                <div className="h-px flex-1 bg-gray-200" />

              </div>

              {/* Google */}

              <button
                type="button"
                onClick={() =>
                  console.log(
                    "Google login clicked"
                  )
                }
                className="flex w-full items-center justify-center gap-3 rounded-xl border border-gray-200 bg-white py-3 text-sm font-medium text-[#202536] transition hover:bg-gray-50"
              >

                <span className="text-base font-bold">
                  G
                </span>

                Continue with Google

              </button>

              {/* Register */}

              <p className="mt-6 text-center text-sm text-[#777B86]">

                Don't have an account?{" "}

                <Link
                  to="/register"
                  className="font-semibold text-[#4662AD] hover:underline"
                >
                  Create account
                </Link>

              </p>

            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default LoginPage;