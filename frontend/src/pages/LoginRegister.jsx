// Combined login and register page.
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

function LoginRegister() {
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const { login, register } = useAuth();
  const navigate = useNavigate();

  function handleChange(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    try {
      if (isRegister) {
        await register(form.username, form.email, form.password);
      } else {
        await login(form.email, form.password);
      }
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="auth-page">
      <form className="card form" onSubmit={handleSubmit}>
        <h2>{isRegister ? "Create account" : "Login"}</h2>
        {error && <p className="error">{error}</p>}

        {isRegister && (
          <label>
            Username
            <input name="username" value={form.username} onChange={handleChange} required />
          </label>
        )}

        <label>
          Email
          <input type="email" name="email" value={form.email} onChange={handleChange} required />
        </label>

        <label>
          Password
          <input type="password" name="password" value={form.password} onChange={handleChange} required />
        </label>

        <button type="submit">{isRegister ? "Register" : "Login"}</button>

        <button type="button" className="link-button center" onClick={() => setIsRegister(!isRegister)}>
          {isRegister ? "Already have an account? Login" : "Need an account? Register"}
        </button>

        <p className="hint">Demo login after seeding: farmer@example.com / password123</p>
      </form>
    </section>
  );
}

export default LoginRegister;
