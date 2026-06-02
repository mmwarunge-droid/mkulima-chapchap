// Simple 404 page.
import { Link } from "react-router-dom";

function NotFound() {
  return (
    <section className="card">
      <h1>Page not found</h1>
      <p>The page you requested does not exist.</p>
      <Link className="button" to="/">Go home</Link>
    </section>
  );
}

export default NotFound;
