import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import api from "../../services/api";

function VerifyEmailPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [status, setStatus] = useState<"loading" | "success" | "error">(
    "loading"
  );
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = searchParams.get("token");

    if (!token) {
      setStatus("error");
      setMessage("Verification token is missing.");
      return;
    }

    const verifyEmail = async () => {
      try {
        const response = await api.get("/api/v1/auths/verify-email", {
          params: {
            token,
          },
        });

        setStatus("success");
        setMessage(
          response.data?.message || "Your email has been verified successfully."
        );
    } catch (error: any) {
        console.error("EMAIL VERIFICATION ERROR:", error);

        console.error("STATUS:", error.response?.status);
        console.error("DATA:", error.response?.data);

       setStatus("error");
       setMessage(
          error.response?.data?.detail ||
         "The verification link is invalid or expired."
        );
      }
    };    

    verifyEmail();
  }, [searchParams]);

  if (status === "loading") {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-[#777B86]">Verifying your email...</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#F2F6FC] px-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 text-center shadow-sm">
        {status === "success" ? (
          <>
            <h1 className="mb-3 text-2xl font-bold text-[#202536]">
              Email Verified!
            </h1>

            <p className="mb-6 text-[#777B86]">
              {message}
            </p>

            <button
              onClick={() => navigate("/login")}
              className="rounded-lg bg-[#4662AD] px-6 py-3 font-medium text-white"
            >
              Go to Login
            </button>
          </>
        ) : (
          <>
            <h1 className="mb-3 text-2xl font-bold text-[#202536]">
              Verification Failed
            </h1>

            <p className="mb-6 text-[#777B86]">
              {message}
            </p>

            <button
              onClick={() => navigate("/login")}
              className="rounded-lg bg-[#4662AD] px-6 py-3 font-medium text-white"
            >
              Go to Login
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default VerifyEmailPage;