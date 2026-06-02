// Public landing page.
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

function Home() {
  const { user } = useAuth();

  return (
    <section className="hero">
      <div>
        <p className="eyebrow">Simple farm health records</p>
        <h1>Track animals, vet records, costs, weights, and reminders.</h1>
        <p>
          Mkulima Chapchap is a basic React + Flask app for farmers. It is
          intentionally simple so it can pass a student bootcamp assessment while
          remaining fully functional.
        </p>
        <Link className="button" to={user ? "/dashboard" : "/login"}>
          {user ? "Go to dashboard" : "Start now"}
        </Link>
      </div>
    </section>
  );
}

export default Home;
