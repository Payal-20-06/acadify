import {
  ArrowRight,
  Eye,
  EyeOff,
  GraduationCap,
  LockKeyhole,
  Mail,
  Phone,
  User,
} from "lucide-react";

import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import {
  registerSchema,
  type RegisterFormData,
} from "../../schemas/authSchema";

import authService from "../../services/authService";
import studentImage from "../../assets/images/student.png";

function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);

  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      role: "student",
      terms: false,
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    try {
      console.log("Register data:", data);

      await authService.register({
        full_name: data.full_name,
        email: data.email,
        phone: data.phone,
        role: data.role,
        password: data.password,
        confirm_password: data.confirm_password,
      });

      console.log("Registration successful");

      navigate("/login");
    } catch (error) {
      console.error("Registration failed:", error);
    }
  };

  return (
    <div className="min-h-screen bg-[#F2F6FC] px-4 py-8">
      <div className="mx-auto flex min-h-[calc(100vh-4rem)] max-w-6xl items-center justify-center">
        <div className="grid w-full overflow-hidden rounded-[32px] bg-white shadow-xl md:grid-cols-2">

          {/* LEFT SIDE */}
          <div className="relative hidden min-h-[700px] overflow-hidden bg-[#F2F6FC] md:flex">
            
            {/* Decorative circles */}
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
                  JOIN ACADIFY
                </p>

                <h1 className="heading-font max-w-md text-4xl font-semibold leading-tight text-[#202536]">
                  Start your academic journey today.
                </h1>

                <p className="mt-4 max-w-md text-sm leading-7 text-[#777B86]">
                  Create your Acadify account and bring your
                  academics, progress and goals together in one
                  simple platform.
                </p>
              </div>

              {/* Illustration */}
              <div className="flex flex-1 items-end justify-center">
                <img
                  src={studentImage}
                  alt="Student"
                  className="max-h-[380px] object-contain"
                />
              </div>

            </div>
          </div>

          {/* RIGHT SIDE */}
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
              <div className="mb-7">
                <p className="mb-2 text-xs font-bold tracking-[0.2em] text-[#55C2C0]">
                  CREATE ACCOUNT
                </p>

                <h2 className="heading-font text-3xl font-semibold text-[#202536]">
                  Welcome to Acadify
                </h2>

                <p className="mt-2 text-sm text-[#777B86]">
                  Create your account to get started.
                </p>
              </div>

              {/* Form */}
              <form
                onSubmit={handleSubmit(onSubmit)}
                className="space-y-4"
              >

                {/* Full Name */}
                <div>
                  <label className="mb-1.5 block text-sm font-medium text-[#202536]">
                    Full name
                  </label>

                  <div className="relative">
                    <User
                      size={17}
                      className="absolute left-3 top-1/2 -translate-y-1/2 text-[#777B86]"
                    />

                    <input
                      type="text"
                      placeholder="Enter your full name"
                      {...register("full_name")}
                      className="w-full rounded-xl border border-gray-200 bg-white py-3 pl-10 pr-4 text-sm outline-none transition focus:border-[#4662AD] focus:ring-2 focus:ring-[#4662AD]/10"
                    />
                  </div>

                  {errors.full_name && (
                    <p className="mt-1 text-xs text-red-500">
                      {errors.full_name.message}
                    </p>
                  )}
                </div>

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

                {/* Phone */}
                <div>
                  <label className="mb-1.5 block text-sm font-medium text-[#202536]">
                    Phone number
                  </label>

                  <div className="relative">
                    <Phone
                      size={17}
                      className="absolute left-3 top-1/2 -translate-y-1/2 text-[#777B86]"
                    />

                    <input
                      type="tel"
                      placeholder="Enter your phone number"
                      {...register("phone")}
                      className="w-full rounded-xl border border-gray-200 bg-white py-3 pl-10 pr-4 text-sm outline-none transition focus:border-[#4662AD] focus:ring-2 focus:ring-[#4662AD]/10"
                    />
                  </div>

                  {errors.phone && (
                    <p className="mt-1 text-xs text-red-500">
                      {errors.phone.message}
                    </p>
                  )}
                </div>

                {/* Role */}
                <div>
                  <label className="mb-1.5 block text-sm font-medium text-[#202536]">
                    I am a
                  </label>

                  <select
                    {...register("role")}
                    className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-[#4662AD] focus:ring-2 focus:ring-[#4662AD]/10"
                  >
                    <option value="student">
                      Student
                    </option>

                    <option value="teacher">
                      Teacher
                    </option>
                  </select>

                  {errors.role && (
                    <p className="mt-1 text-xs text-red-500">
                      {errors.role.message}
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
                      placeholder="Create a password"
                      {...register("password")}
                      className="w-full rounded-xl border border-gray-200 bg-white py-3 pl-10 pr-11 text-sm outline-none transition focus:border-[#4662AD] focus:ring-2 focus:ring-[#4662AD]/10"
                    />

                    <button
                      type="button"
                      onClick={() =>
                        setShowPassword(!showPassword)
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

                {/* Confirm Password */}
                <div>
                  <label className="mb-1.5 block text-sm font-medium text-[#202536]">
                    Confirm password
                  </label>

                  <div className="relative">
                    <LockKeyhole
                      size={17}
                      className="absolute left-3 top-1/2 -translate-y-1/2 text-[#777B86]"
                    />

                    <input
                      type={
                        showConfirmPassword
                          ? "text"
                          : "password"
                      }
                      placeholder="Confirm your password"
                      {...register("confirm_password")}
                      className="w-full rounded-xl border border-gray-200 bg-white py-3 pl-10 pr-11 text-sm outline-none transition focus:border-[#4662AD] focus:ring-2 focus:ring-[#4662AD]/10"
                    />

                    <button
                      type="button"
                      onClick={() =>
                        setShowConfirmPassword(
                          !showConfirmPassword
                        )
                      }
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-[#777B86] hover:text-[#4662AD]"
                    >
                      {showConfirmPassword ? (
                        <EyeOff size={17} />
                      ) : (
                        <Eye size={17} />
                      )}
                    </button>
                  </div>

                  {errors.confirm_password && (
                    <p className="mt-1 text-xs text-red-500">
                      {errors.confirm_password.message}
                    </p>
                  )}
                </div>

                {/* Terms */}
                <div>
                  <label className="flex cursor-pointer items-start gap-2">
                    <input
                      type="checkbox"
                      {...register("terms")}
                      className="mt-0.5 h-4 w-4 rounded border-gray-300 accent-[#4662AD]"
                    />

                    <span className="text-xs leading-5 text-[#777B86]">
                      I agree to the terms and conditions.
                    </span>
                  </label>

                  {errors.terms && (
                    <p className="mt-1 text-xs text-red-500">
                      {errors.terms.message}
                    </p>
                  )}
                </div>

                {/* Submit */}
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-[#4662AD] py-3 text-sm font-semibold text-white transition hover:bg-[#3d579c] disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {isSubmitting
                    ? "Creating account..."
                    : "Create account"}

                  {!isSubmitting && (
                    <ArrowRight size={17} />
                  )}
                </button>
              </form>

              {/* Login */}
              <p className="mt-6 text-center text-sm text-[#777B86]">
                Already have an account?{" "}
                <Link
                  to="/login"
                  className="font-semibold text-[#4662AD] hover:underline"
                >
                  Sign in
                </Link>
              </p>

            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default RegisterPage;