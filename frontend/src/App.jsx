// Defines the application's pages and routes.
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import Home from "./pages/Home.jsx";
import LoginRegister from "./pages/LoginRegister.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import AnimalDetails from "./pages/AnimalDetails.jsx";
import NotFound from "./pages/NotFound.jsx";

function App() {
  return (
    <>
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginRegister />} />

          {/* Protected pages: only logged-in users can access them. */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/animals/:id"
            element={
              <ProtectedRoute>
                <AnimalDetails />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
