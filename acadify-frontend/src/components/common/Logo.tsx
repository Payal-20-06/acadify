import { GraduationCap } from "lucide-react";

interface LogoProps {
  dark?: boolean;
}

function Logo({ dark = false }: LogoProps) {
  return (
    <div className="flex items-center gap-2">
      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm">
        <GraduationCap size={21} strokeWidth={2.5} />
      </div>

      <span
        className={`text-xl font-extrabold tracking-tight ${
          dark ? "text-white" : "text-[#101936]"
        }`}
      >
        Acadify
      </span>
    </div>
  );
}

export default Logo;