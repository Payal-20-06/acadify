import {
  Sun,
} from "lucide-react";
import Logo from "./Logo";

function Navbar() {
  return (
    <header className="absolute left-0 right-0 top-0 z-50 px-4 py-4">
      <nav className="mx-auto flex max-w-7xl items-center justify-between rounded-2xl border border-white/70 bg-white/85 px-5 py-3 shadow-sm backdrop-blur-md">

        <Logo />

        <div className="hidden items-center gap-7 lg:flex">
          <a
            href="#home"
            className="rounded-full bg-blue-50 px-3 py-1.5 text-sm font-semibold text-blue-700"
          >
            Home
          </a>

          <a
            href="#features"
            className="text-sm font-medium text-[#283557] transition hover:text-blue-600"
          >
            Features
          </a>

          <a
            href="#students"
            className="text-sm font-medium text-[#283557] transition hover:text-blue-600"
          >
            For Students
          </a>

          <a
            href="#teachers"
            className="text-sm font-medium text-[#283557] transition hover:text-blue-600"
          >
            For Teachers
          </a>

          <a
            href="#pricing"
            className="text-sm font-medium text-[#283557] transition hover:text-blue-600"
          >
            Pricing
          </a>
        </div>

        <div className="flex items-center gap-2">
          <button
            className="hidden h-10 w-10 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-600 transition hover:bg-slate-50 md:flex"
            aria-label="Toggle theme"
          >
            <Sun size={18} />
          </button>

          <a
            href="/login"
            className="hidden rounded-full border border-slate-200 bg-white px-5 py-2.5 text-sm font-semibold text-[#101936] transition hover:bg-slate-50 sm:block"
          >
            Login
          </a>

          <a
            href="/register"
            className="rounded-full bg-[#17233f] px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-slate-300 transition hover:-translate-y-0.5 hover:bg-[#101a32]"
          >
            Get Started
            <span className="ml-2">→</span>
          </a>
        </div>
      </nav>
    </header>
  );
}

export default Navbar;