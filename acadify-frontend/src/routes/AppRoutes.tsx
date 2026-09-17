import { Route, Routes } from "react-router-dom";

import LandingPage from "../pages/public/LandingPage";
import LoginPage from "../pages/auth/LoginPage";
import RegisterPage from "../pages/auth/RegisterPage";

function AppRoutes() {
  return (
    <Routes>

      {/* Public */}
      <Route path="/" element={<LandingPage />} />

      {/* Authentication */}
      <Route path="/login" element={<LoginPage />} />

       <Route path="/register" element={<RegisterPage />} />

    </Routes>
  );
}

export default AppRoutes;