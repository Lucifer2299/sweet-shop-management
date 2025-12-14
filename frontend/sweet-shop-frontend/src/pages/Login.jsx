import { useState } from "react";
import api from "../api/api";
import "../styles/auth.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const login = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/api/auth/login", { email, password });
      localStorage.setItem("access_token", res.data.access_token);
      window.location.href = "/sweets";
    } catch {
      setError("Login failed");
    }
  };

  return (
    <div className="auth">
      <form className="auth-card" onSubmit={login}>
        <h2>Sweet Shop Login</h2>
        {error && <p className="error">{error}</p>}
        <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
        <input type="password" placeholder="Password"
               onChange={e => setPassword(e.target.value)} />
        <button>Login</button>
        <p onClick={() => window.location.href="/register"} className="link">
          Create account
        </p>
      </form>
    </div>
  );
}

