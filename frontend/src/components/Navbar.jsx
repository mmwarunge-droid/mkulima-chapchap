// Shared navigation bar.
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/");
  }

  return (
    <header className="navbar">
      <Link className="logo" to="/">Mkulima Chapchap</Link>
      <nav>
        <NavLink to="/">Home</NavLink>
        {user ? (
          <>
            <NavLink to="/dashboard">Dashboard</NavLink>
            <button className="link-button" onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <NavLink to="/login">Login/Register</NavLink>
        )}
      </nav>
    </header>
  );
}

export default Navbar;
