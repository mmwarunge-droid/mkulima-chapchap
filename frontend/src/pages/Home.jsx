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
          Mkulima Chapchap helps you keep track of your farm's health records in one place, so you can focus on what matters most: your animals and your farm.
        </p>
        <Link className="button" to={user ? "/dashboard" : "/login"}>
          {user ? "Go to dashboard" : "Start now"}
        </Link>
      </div>
    </section>
  );
}

export default Home;
