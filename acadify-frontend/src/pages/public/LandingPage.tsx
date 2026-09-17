import {
  ArrowRight,
  BarChart3,
  BookOpen,
  CalendarCheck,
  Check,
  ChevronDown,
  ClipboardList,
  GraduationCap,
  Menu,
  Sparkles,
  Users,
} from "lucide-react";

import { useState, type ReactNode } from "react";

import studentImage from "../../assets/images/student.png";
import teacherImage from "../../assets/images/teacher.png";
import adminImage from "../../assets/images/admin.png";

function LandingPage() {
  const [mobileMenu, setMobileMenu] = useState(false);

  return (
    <div className="min-h-screen overflow-x-hidden bg-white text-[#202536]">

      {/* ========================= NAVBAR ========================= */}

      <header className="sticky top-0 z-50 px-4 pt-4">
        <nav className="mx-auto flex max-w-7xl items-center justify-between rounded-2xl bg-white px-5 py-3 shadow-[0_4px_20px_rgba(32,37,54,0.08)]">

          <a href="/" className="flex items-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#4662AD] text-white">
              <GraduationCap size={21} />
            </div>

            <span className="text-lg font-bold tracking-tight">
              Acadify
            </span>
          </a>

          <div className="hidden items-center gap-8 text-sm font-medium text-[#777B86] lg:flex">
            <a
              href="#features"
              className="transition hover:text-[#4662AD]"
            >
              Features
            </a>

            <a
              href="#how-it-works"
              className="transition hover:text-[#4662AD]"
            >
              How it works
            </a>

            <a
              href="#roles"
              className="transition hover:text-[#4662AD]"
            >
              For everyone
            </a>

            <a
              href="#faq"
              className="transition hover:text-[#4662AD]"
            >
              FAQ
            </a>
          </div>

          <div className="hidden items-center gap-3 lg:flex">
            <a
              href="/login"
              className="rounded-xl px-4 py-2 text-sm font-semibold text-[#4D5361] hover:text-[#4662AD]"
            >
              Log in
            </a>

            <a
              href="/register"
              className="flex items-center gap-2 rounded-xl bg-[#4662AD] px-5 py-2.5 text-sm font-bold text-white shadow-md shadow-[#4662AD]/20 transition hover:-translate-y-0.5"
            >
              Get Started
              <ArrowRight size={15} />
            </a>
          </div>

          <button
            onClick={() => setMobileMenu(!mobileMenu)}
            className="rounded-lg p-2 lg:hidden"
          >
            <Menu size={22} />
          </button>
        </nav>

        {mobileMenu && (
          <div className="mx-auto mt-2 max-w-7xl rounded-2xl bg-white p-5 shadow-lg lg:hidden">
            <div className="flex flex-col gap-4 text-sm font-semibold">

              <a href="#features">Features</a>
              <a href="#how-it-works">How it works</a>
              <a href="#roles">For everyone</a>
              <a href="#faq">FAQ</a>

              <hr className="border-[#E7EAF0]" />

              <a href="/login">
                Log in
              </a>

              <a
                href="/register"
                className="rounded-xl bg-[#4662AD] px-4 py-3 text-center text-white"
              >
                Get Started
              </a>

            </div>
          </div>
        )}
      </header>


      {/* =========================== HERO ========================== */}

      <section className="relative overflow-hidden px-4 pb-20 pt-14 sm:pt-20 lg:pb-28">

        <div className="absolute -left-24 top-28 h-64 w-64 rounded-full bg-[#E8F7F7]" />

        <div className="absolute right-[-80px] top-12 h-60 w-60 rounded-full bg-[#FFF3D8]" />

        <div className="relative mx-auto grid max-w-7xl items-center gap-12 lg:grid-cols-2">

          {/* Hero Content */}

          <div className="relative z-10">

            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-[#D8E3F6] bg-[#F2F6FC] px-4 py-2 text-xs font-semibold text-[#4662AD]">

              <Sparkles size={13} />

              A smarter way to manage academics

            </div>


            <h1 className="heading-font max-w-xl text-5xl font-semibold leading-[1.08] tracking-[-0.02em] sm:text-6xl lg:text-[64px]">

              Learn better.

              <br />

              <span className="text-[#4662AD]">
                Track progress.
              </span>

              <br />

              Achieve more.

            </h1>


            <p className="mt-6 max-w-lg text-base leading-7 text-[#777B86] sm:text-lg">

              Acadify brings your academic life together in one simple
              platform. Manage subjects, grades, attendance and
              assignments while keeping your progress clear and organized.

            </p>


            <div className="mt-8 flex flex-wrap gap-3">

              <a
                href="/register"
                className="flex items-center gap-2 rounded-xl bg-[#4662AD] px-6 py-3.5 text-sm font-bold text-white shadow-lg shadow-[#4662AD]/20 transition hover:-translate-y-0.5"
              >
                Get Started
                <ArrowRight size={17} />
              </a>

              <a
                href="#features"
                className="rounded-xl border border-[#DDE2EA] bg-white px-6 py-3.5 text-sm font-bold text-[#4D5361] transition hover:border-[#4662AD] hover:text-[#4662AD]"
              >
                Explore Acadify
              </a>

            </div>

          </div>


          {/* Hero Illustration */}

          <div className="relative flex justify-center lg:justify-end">

            <div className="absolute right-8 top-2 h-20 w-20 rounded-full bg-[#F7C95C]" />

            <div className="absolute bottom-12 left-5 h-20 w-20 rounded-full bg-[#55C2C0]" />

            <div className="absolute right-0 top-32 h-14 w-14 rotate-12 rounded-2xl bg-[#F58B35]" />

            <div className="relative w-full max-w-[560px]">

              <div className="absolute inset-8 rounded-[45%] bg-[#E8F7F7]" />

              <div className="relative flex min-h-[460px] items-end justify-center overflow-hidden rounded-[45%_45%_35%_35%] bg-[#F2F6FC] px-5 pt-12">

                <div className="absolute left-5 top-24 z-20 rounded-xl bg-white px-3 py-2 text-xs font-bold text-[#4662AD] shadow-md">
                  Grades
                </div>

                <div className="absolute right-5 top-44 z-20 rounded-xl bg-white px-3 py-2 text-xs font-bold text-[#55A9A7] shadow-md">
                  Progress
                </div>

                <div className="absolute left-12 top-52 z-20 rounded-xl bg-[#F58B35] px-3 py-2 text-xs font-bold text-white shadow-md">
                  Learn
                </div>

                <img
                  src={studentImage}
                  alt="Acadify student"
                  className="relative z-10 max-h-[470px] w-auto object-contain"
                />

              </div>

              <p className="handwritten absolute right-1 top-1 z-30 rotate-[-7deg] text-xl text-[#4662AD] sm:text-2xl">
                Learn.
                <br />
                Track.
                <br />
                Grow. ♡
              </p>

            </div>
          </div>

        </div>
      </section>


      {/* ========================= WHAT WE DO ====================== */}

      <section className="relative overflow-hidden px-4 py-20 sm:py-28">

        <div className="mx-auto max-w-6xl">

          <div className="text-center">

            <p className="text-[10px] font-bold uppercase tracking-[0.25em] text-[#55A9A7]">
              WHAT WE DO
            </p>

            <h2 className="heading-font mt-3 text-4xl font-semibold leading-tight sm:text-5xl">
              Everything you need
              <br />
              to move forward.
            </h2>

            <p className="mx-auto mt-5 max-w-2xl text-sm leading-7 text-[#777B86]">
              From everyday learning to long-term progress, Acadify helps
              you stay organized, informed and focused on what matters.
            </p>

          </div>


          <div className="mt-16 grid gap-12 md:grid-cols-3">

            <OfferCard
              number="01"
              icon={<BookOpen size={27} />}
              title="Learn"
              text="Stay organized with your subjects, assignments and academic information."
              iconClass="bg-[#E8F7F7] text-[#55A9A7]"
            />

            <OfferCard
              number="02"
              icon={<BarChart3 size={27} />}
              title="Track"
              text="Keep an eye on grades, attendance and your overall performance."
              iconClass="bg-[#EEF2FB] text-[#4662AD]"
            />

            <OfferCard
              number="03"
              icon={<Sparkles size={27} />}
              title="Grow"
              text="Understand your progress and take the next step with confidence."
              iconClass="bg-[#FFF3D8] text-[#F58B35]"
            />

          </div>

        </div>
      </section>


      {/* =========================== FEATURES ====================== */}

      <section
        id="features"
        className="relative overflow-hidden bg-[#F2F6FC] px-4 py-20 sm:py-28"
      >

        <div className="mx-auto max-w-7xl">

          <div className="max-w-2xl">

            <p className="text-[10px] font-bold uppercase tracking-[0.25em] text-[#55A9A7]">
              LEARN MORE
            </p>

            <h2 className="heading-font mt-3 text-4xl font-semibold leading-tight sm:text-5xl">
              Your academics.
              <br />
              All in one place.
            </h2>

            <p className="mt-5 max-w-xl text-sm leading-7 text-[#777B86]">
              Acadify makes it easier to manage the things that matter
              throughout your academic journey.
            </p>

          </div>


          <div className="mt-12 grid gap-5 md:grid-cols-2 lg:grid-cols-3">

            <FeatureCard
              icon={<BarChart3 />}
              title="Performance"
              text="Understand your grades and see how your academic performance changes over time."
              bg="bg-white"
              iconBg="bg-[#EEF2FB]"
              iconColor="text-[#4662AD]"
            />

            <FeatureCard
              icon={<CalendarCheck />}
              title="Attendance"
              text="Stay aware of your attendance and never lose track of your participation."
              bg="bg-[#E8F7F7]"
              iconBg="bg-white"
              iconColor="text-[#55A9A7]"
            />

            <FeatureCard
              icon={<ClipboardList />}
              title="Assignments"
              text="Keep upcoming work, deadlines and academic tasks organized."
              bg="bg-[#FFF3D8]"
              iconBg="bg-white"
              iconColor="text-[#F58B35]"
            />

            <FeatureCard
              icon={<BookOpen />}
              title="Subjects"
              text="Access everything you need for the subjects you're studying."
              bg="bg-white"
              iconBg="bg-[#FFF3D8]"
              iconColor="text-[#F0A83A]"
            />

            <FeatureCard
              icon={<Users />}
              title="Smart Dashboards"
              text="See the information that matters most to your role at a glance."
              bg="bg-[#EEF7ED]"
              iconBg="bg-white"
              iconColor="text-[#68CC7A]"
            />

            <FeatureCard
              icon={<GraduationCap />}
              title="Academic Insights"
              text="Turn your academic activity into a clearer picture of your progress."
              bg="bg-white"
              iconBg="bg-[#E8F7F7]"
              iconColor="text-[#55A9A7]"
            />

          </div>

        </div>
      </section>


      {/* =========================== BENEFITS ====================== */}

      <section className="relative overflow-hidden px-4 py-20 sm:py-28">

        <div className="mx-auto grid max-w-7xl items-center gap-14 lg:grid-cols-2">

          <div className="relative flex justify-center">

            <div className="absolute bottom-0 h-72 w-72 rounded-full bg-[#E8F7F7]" />

            <div className="absolute left-10 top-10 h-16 w-16 rounded-full bg-[#F7C95C]" />

            <div className="absolute right-10 top-20 h-14 w-14 rounded-full bg-[#4662AD]" />

            <div className="relative z-10 flex min-h-[430px] items-end justify-center">

              <img
                src={teacherImage}
                alt="Acadify teacher"
                className="max-h-[430px] object-contain"
              />

            </div>

          </div>


          <div>

            <p className="text-[10px] font-bold uppercase tracking-[0.25em] text-[#55A9A7]">
              WHY ACADIFY
            </p>

            <h2 className="heading-font mt-3 text-4xl font-semibold leading-tight sm:text-5xl">
              A better way to
              <br />
              manage academic life.
            </h2>

            <p className="mt-5 max-w-lg text-sm leading-7 text-[#777B86]">
              Whether you're a student, teacher or administrator, Acadify
              gives you a simple way to stay connected with the academic
              journey.
            </p>

            <div className="mt-8 grid gap-4 sm:grid-cols-2">

              <Benefit text="Everything in one place" />
              <Benefit text="Know where you stand" />
              <Benefit text="Stay ahead of deadlines" />
              <Benefit text="Simplify attendance tracking" />
              <Benefit text="Make better decisions" />
              <Benefit text="Designed for every role" />

            </div>

          </div>

        </div>
      </section>


      {/* ========================= HOW IT WORKS ==================== */}

      <section
        id="how-it-works"
        className="relative overflow-hidden bg-[#FFF8E8] px-4 py-20 sm:py-28"
      >

        <div className="mx-auto max-w-6xl">

          <div className="text-center">

            <p className="text-[10px] font-bold uppercase tracking-[0.25em] text-[#F58B35]">
              HOW IT WORKS
            </p>

            <h2 className="heading-font mt-3 text-4xl font-semibold sm:text-5xl">
              Getting started is simple.
            </h2>

          </div>


          <div className="mt-14 grid gap-7 md:grid-cols-3">

            <StepCard
              number="01"
              title="Choose your role"
              text="Start with the experience designed for you — Student, Teacher or Administrator."
              color="bg-[#4662AD]"
            />

            <StepCard
              number="02"
              title="Manage your academics"
              text="Access the tools you need to manage grades, attendance, assignments and subjects."
              color="bg-[#55C2C0]"
            />

            <StepCard
              number="03"
              title="Track your progress"
              text="See your academic journey clearly and keep moving toward your goals."
              color="bg-[#F58B35]"
            />

          </div>

        </div>
      </section>


      {/* ============================= ROLES ======================= */}

      <section
        id="roles"
        className="px-4 py-20 sm:py-28"
      >

        <div className="mx-auto max-w-7xl">

          <div className="text-center">

            <p className="text-[10px] font-bold uppercase tracking-[0.25em] text-[#55A9A7]">
              FOR EVERYONE
            </p>

            <h2 className="heading-font mt-3 text-4xl font-semibold sm:text-5xl">
              One platform.
              <br />
              Made for every academic journey.
            </h2>

            <p className="mx-auto mt-5 max-w-xl text-sm leading-6 text-[#777B86]">
              Acadify adapts to the people using it, giving every role
              the tools they need.
            </p>

          </div>


          <div className="mt-12 grid gap-6 lg:grid-cols-3">

            <RoleCard
              title="Student"
              description="Take control of your learning."
              image={studentImage}
              bg="bg-[#EEF7ED]"
              accent="#68CC7A"
              items={[
                "Grades",
                "Attendance",
                "Assignments",
                "Performance",
              ]}
            />

            <RoleCard
              title="Teacher"
              description="Make teaching more organized."
              image={teacherImage}
              bg="bg-[#EEF2FB]"
              accent="#4662AD"
              items={[
                "Students",
                "Grades",
                "Attendance",
                "Assignments",
              ]}
            />

            <RoleCard
              title="Admin"
              description="Keep your institution connected."
              image={adminImage}
              bg="bg-[#FFF3D8]"
              accent="#F58B35"
              items={[
                "Users",
                "Teachers",
                "Students",
                "Reports",
              ]}
            />

          </div>

        </div>
      </section>


      {/* ========================= DASHBOARD ====================== */}

      <section className="bg-[#F2F6FC] px-4 py-20 sm:py-28">

        <div className="mx-auto grid max-w-7xl items-center gap-12 lg:grid-cols-[0.8fr_1.2fr]">

          <div>

            <p className="text-[10px] font-bold uppercase tracking-[0.25em] text-[#4662AD]">
              YOUR ACADEMIC SPACE
            </p>

            <h2 className="heading-font mt-3 text-4xl font-semibold leading-tight sm:text-5xl">
              Know where you are.
              <br />
              Know where you're going.
            </h2>

            <p className="mt-5 max-w-lg text-sm leading-7 text-[#777B86]">
              Your Acadify dashboard brings your important academic
              information together so you can spend less time searching
              and more time moving forward.
            </p>

            <div className="mt-8 space-y-4">

              <Benefit text="Clear academic overview" />
              <Benefit text="Visual performance trends" />
              <Benefit text="Upcoming assignments" />
              <Benefit text="Recent academic activity" />

            </div>

          </div>


          <div className="rounded-[30px] bg-white p-3 shadow-[0_20px_60px_rgba(70,98,173,0.12)]">

            <div className="overflow-hidden rounded-[22px] bg-[#F7F9FC]">

              <div className="flex items-center gap-1.5 border-b border-[#E5E9F0] bg-white px-4 py-3">

                <span className="h-2.5 w-2.5 rounded-full bg-[#55C2C0]" />
                <span className="h-2.5 w-2.5 rounded-full bg-[#F7C95C]" />
                <span className="h-2.5 w-2.5 rounded-full bg-[#F58B35]" />

              </div>


              <div className="grid grid-cols-[110px_1fr]">

                <div className="border-r border-[#E5E9F0] bg-white p-3">

                  <div className="mb-6 flex items-center gap-1.5">

                    <div className="flex h-5 w-5 items-center justify-center rounded-md bg-[#4662AD] text-white">
                      <GraduationCap size={11} />
                    </div>

                    <span className="text-[8px] font-bold">
                      Acadify
                    </span>

                  </div>

                  <div className="space-y-2">

                    {[
                      "Dashboard",
                      "Subjects",
                      "Grades",
                      "Attendance",
                      "Assignments",
                    ].map((item, index) => (

                      <div
                        key={item}
                        className={`rounded-lg px-2 py-2 text-[8px] font-semibold ${
                          index === 0
                            ? "bg-[#EEF2FB] text-[#4662AD]"
                            : "text-[#A0A6B1]"
                        }`}
                      >
                        {item}
                      </div>

                    ))}

                  </div>

                </div>


                <div className="p-5">

                  <p className="text-[8px] text-[#A0A6B1]">
                    Student Dashboard
                  </p>

                  <h3 className="mt-1 text-sm font-extrabold">
                    Good morning!
                  </h3>


                  <div className="mt-4 grid grid-cols-3 gap-2">

                    <MiniStat
                      title="GPA"
                      value="8.42"
                      bg="bg-[#EEF2FB]"
                    />

                    <MiniStat
                      title="Attendance"
                      value="91%"
                      bg="bg-[#E8F7F7]"
                    />

                    <MiniStat
                      title="Tasks"
                      value="4"
                      bg="bg-[#FFF3D8]"
                    />

                  </div>


                  <div className="mt-3 grid grid-cols-2 gap-2">

                    <div className="h-32 rounded-xl bg-white p-3">

                      <p className="text-[8px] font-bold">
                        Performance
                      </p>

                      <div className="mt-5 flex h-20 items-end gap-1">

                        {[30, 45, 38, 58, 52, 72, 66, 82].map(
                          (height, index) => (

                            <div
                              key={index}
                              style={{
                                height: `${height}%`,
                              }}
                              className={`flex-1 rounded-t ${
                                index % 3 === 0
                                  ? "bg-[#4662AD]"
                                  : index % 3 === 1
                                    ? "bg-[#55C2C0]"
                                    : "bg-[#F7C95C]"
                              }`}
                            />

                          )
                        )}

                      </div>

                    </div>


                    <div className="h-32 rounded-xl bg-white p-3">

                      <p className="text-[8px] font-bold">
                        Recent Grades
                      </p>

                      <div className="mt-4 space-y-3">

                        <GradeRow
                          subject="Mathematics"
                          grade="A"
                        />

                        <GradeRow
                          subject="Physics"
                          grade="A-"
                        />

                        <GradeRow
                          subject="Data Science"
                          grade="A+"
                        />

                      </div>

                    </div>

                  </div>

                </div>

              </div>

            </div>

          </div>

        </div>
      </section>


      {/* ============================== FAQ ======================== */}

      <section
        id="faq"
        className="px-4 py-20 sm:py-28"
      >

        <div className="mx-auto max-w-4xl">

          <div className="text-center">

            <p className="text-[10px] font-bold uppercase tracking-[0.25em] text-[#55A9A7]">
              FAQ
            </p>

            <h2 className="heading-font mt-3 text-4xl font-semibold sm:text-5xl">
              Have questions?
              <br />
              We're here to help.
            </h2>

          </div>


          <div className="mt-10 divide-y divide-[#E5E9F0]">

            <FAQ
              question="Who is Acadify for?"
              answer="Acadify is designed for students, teachers and administrators."
            />

            <FAQ
              question="Can each role have a different dashboard?"
              answer="Yes. Students, teachers and administrators can have different dashboards and features based on their responsibilities."
            />

            <FAQ
              question="What can students manage on Acadify?"
              answer="Students can view and manage academic information such as grades, attendance, subjects and assignments."
            />

            <FAQ
              question="What can teachers manage?"
              answer="Teachers can manage students, grades, attendance and assignments."
            />

            <FAQ
              question="What can administrators manage?"
              answer="Administrators can manage users, students, teachers, subjects and academic reports."
            />

          </div>

        </div>
      </section>


      {/* ============================== CTA ======================== */}

      <section className="px-4 pb-20">

        <div className="relative mx-auto max-w-7xl overflow-hidden rounded-[38px] bg-[#4662AD] px-7 py-16 text-center text-white sm:px-12">

          <div className="absolute -left-12 -top-12 h-40 w-40 rounded-full bg-[#55C2C0]/30" />

          <div className="absolute -bottom-12 -right-12 h-48 w-48 rounded-full bg-[#F7C95C]/30" />

          <div className="relative">

            <p className="handwritten text-2xl text-[#F7C95C]">
              Ready to get started?
            </p>

            <h2 className="heading-font mx-auto mt-3 max-w-3xl text-4xl font-semibold sm:text-5xl lg:text-6xl">
              Your academic journey starts here.
            </h2>

            <p className="mx-auto mt-5 max-w-xl text-sm leading-6 text-white/75 sm:text-base">
              Organize your academics, track your progress and keep
              moving toward your goals with Acadify.
            </p>

            <div className="mt-8 flex flex-wrap justify-center gap-3">

              <a
                href="/register"
                className="flex items-center gap-2 rounded-xl bg-white px-6 py-3.5 text-sm font-bold text-[#4662AD] shadow-lg transition hover:-translate-y-0.5"
              >
                Get Started
                <ArrowRight size={16} />
              </a>

              <a
                href="/login"
                className="rounded-xl border border-white/30 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-white/10"
              >
                Log in
              </a>

            </div>

          </div>

        </div>
      </section>


      {/* ============================ FOOTER ======================= */}

      <footer className="border-t border-[#E7EAF0] bg-white px-4 py-12">

        <div className="mx-auto grid max-w-7xl gap-10 sm:grid-cols-2 lg:grid-cols-4">

          <div>

            <div className="flex items-center gap-2">

              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#4662AD] text-white">
                <GraduationCap size={19} />
              </div>

              <span className="font-bold">
                Acadify
              </span>

            </div>

            <p className="mt-4 max-w-xs text-sm leading-6 text-[#A0A6B1]">
              Track. Learn. Achieve.
              <br />
              A simpler way to manage academic life.
            </p>

          </div>


          <FooterColumn
            title="Product"
            links={[
              "Features",
              "How it works",
              "Dashboard",
            ]}
          />

          <FooterColumn
            title="Platform"
            links={[
              "Students",
              "Teachers",
              "Administrators",
            ]}
          />

          <FooterColumn
            title="Company"
            links={[
              "About",
              "Contact",
              "Privacy",
            ]}
          />

        </div>


        <div className="mx-auto mt-10 max-w-7xl border-t border-[#E7EAF0] pt-6 text-xs text-[#A0A6B1]">
          © 2026 Acadify. All rights reserved.
        </div>

      </footer>

    </div>
  );
}


/* ========================================================= */
/* OFFER CARD                                                  */
/* ========================================================= */

function OfferCard({
  number,
  icon,
  title,
  text,
  iconClass,
}: {
  number: string;
  icon: ReactNode;
  title: string;
  text: string;
  iconClass: string;
}) {
  return (
    <div className="text-center">

      <div
        className={`mx-auto flex h-16 w-16 items-center justify-center rounded-2xl ${iconClass}`}
      >
        {icon}
      </div>

      <p className="mt-5 text-xs font-bold text-[#A0A6B1]">
        {number}
      </p>

      <h3 className="mt-2 text-xl font-bold">
        {title}
      </h3>

      <p className="mx-auto mt-3 max-w-xs text-sm leading-6 text-[#777B86]">
        {text}
      </p>

    </div>
  );
}


/* ========================================================= */
/* FEATURE CARD                                                */
/* ========================================================= */

function FeatureCard({
  icon,
  title,
  text,
  bg,
  iconBg,
  iconColor,
}: {
  icon: ReactNode;
  title: string;
  text: string;
  bg: string;
  iconBg: string;
  iconColor: string;
}) {
  return (
    <div
      className={`min-h-[230px] rounded-[28px] p-7 ${bg} transition hover:-translate-y-1 hover:shadow-[0_15px_40px_rgba(32,37,54,0.08)]`}
    >

      <div
        className={`flex h-12 w-12 items-center justify-center rounded-full ${iconBg} ${iconColor}`}
      >
        {icon}
      </div>

      <h3 className="mt-12 text-xl font-bold">
        {title}
      </h3>

      <p className="mt-3 max-w-sm text-sm leading-6 text-[#777B86]">
        {text}
      </p>

    </div>
  );
}


/* ========================================================= */
/* BENEFIT                                                      */
/* ========================================================= */

function Benefit({ text }: { text: string }) {
  return (
    <div className="flex items-center gap-3">

      <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[#E8F7F7] text-[#55A9A7]">
        <Check size={13} strokeWidth={3} />
      </div>

      <span className="text-sm font-semibold text-[#4D5361]">
        {text}
      </span>

    </div>
  );
}


/* ========================================================= */
/* STEP CARD                                                    */
/* ========================================================= */

function StepCard({
  number,
  title,
  text,
  color,
}: {
  number: string;
  title: string;
  text: string;
  color: string;
}) {
  return (
    <div className="rounded-[28px] bg-white p-7 shadow-[0_8px_30px_rgba(32,37,54,0.06)]">

      <div
        className={`flex h-12 w-12 items-center justify-center rounded-full ${color} text-sm font-bold text-white`}
      >
        {number}
      </div>

      <h3 className="mt-7 text-xl font-bold">
        {title}
      </h3>

      <p className="mt-3 text-sm leading-6 text-[#777B86]">
        {text}
      </p>

    </div>
  );
}


/* ========================================================= */
/* ROLE CARD                                                     */
/* ========================================================= */

function RoleCard({
  title,
  description,
  image,
  bg,
  accent,
  items,
}: {
  title: string;
  description: string;
  image: string;
  bg: string;
  accent: string;
  items: string[];
}) {
  return (
    <div
      className={`relative overflow-hidden rounded-[30px] ${bg} p-7`}
    >

      <div className="flex items-start justify-between">

        <div>

          <p
            className="text-[10px] font-bold uppercase tracking-[0.2em]"
            style={{ color: accent }}
          >
            ACADIFY
          </p>

          <h3 className="mt-2 text-2xl font-bold">
            {title}
          </h3>

        </div>

        <ArrowRight
          size={19}
          style={{ color: accent }}
        />

      </div>


      <p className="mt-4 max-w-xs text-sm leading-6 text-[#777B86]">
        {description}
      </p>


      <div className="mt-5 flex flex-wrap gap-2">

        {items.map((item) => (
          <span
            key={item}
            className="rounded-full bg-white/80 px-3 py-1.5 text-[10px] font-semibold text-[#59606D]"
          >
            {item}
          </span>
        ))}

      </div>


      <div className="mt-4 flex h-64 items-end justify-center">

        <img
          src={image}
          alt={`Acadify ${title}`}
          className="max-h-64 object-contain transition duration-300 hover:scale-105"
        />

      </div>

    </div>
  );
}


/* ========================================================= */
/* MINI STAT                                                     */
/* ========================================================= */

function MiniStat({
  title,
  value,
  bg,
}: {
  title: string;
  value: string;
  bg: string;
}) {
  return (
    <div className={`rounded-xl ${bg} p-3`}>

      <p className="text-[9px] text-[#777B86]">
        {title}
      </p>

      <p className="mt-1 text-lg font-bold">
        {value}
      </p>

    </div>
  );
}


/* ========================================================= */
/* GRADE ROW                                                     */
/* ========================================================= */

function GradeRow({
  subject,
  grade,
}: {
  subject: string;
  grade: string;
}) {
  return (
    <div className="flex items-center justify-between">

      <span className="text-[8px] text-[#777B86]">
        {subject}
      </span>

      <span className="text-[9px] font-bold text-[#4662AD]">
        {grade}
      </span>

    </div>
  );
}


/* ========================================================= */
/* FAQ                                                           */
/* ========================================================= */

function FAQ({
  question,
  answer,
}: {
  question: string;
  answer: string;
}) {
  return (
    <details className="group py-6">

      <summary className="flex cursor-pointer list-none items-center justify-between gap-5 font-semibold">

        <span>
          {question}
        </span>

        <ChevronDown
          size={18}
          className="shrink-0 transition group-open:rotate-180"
        />

      </summary>

      <p className="mt-4 max-w-3xl text-sm leading-6 text-[#777B86]">
        {answer}
      </p>

    </details>
  );
}


/* ========================================================= */
/* FOOTER COLUMN                                                */
/* ========================================================= */

function FooterColumn({
  title,
  links,
}: {
  title: string;
  links: string[];
}) {
  return (
    <div>

      <h4 className="text-sm font-bold">
        {title}
      </h4>

      <div className="mt-4 space-y-3">

        {links.map((link) => (
          <a
            key={link}
            href="#"
            className="block text-sm text-[#A0A6B1] transition hover:text-[#4662AD]"
          >
            {link}
          </a>
        ))}

      </div>

    </div>
  );
}


export default LandingPage;