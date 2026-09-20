import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const { data } = await api.post("/auth/login/", form);
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      navigate("/dashboard");
    } catch {
      setError("Couldn't sign you in — check your username and password.");
    }
  };

  return (
    <div className="max-w-md mx-auto px-6 py-20">
      <h1 className="font-display text-3xl text-ink mb-2">Welcome back</h1>
      <p className="text-inkmuted mb-8">Sign in to check your scores, draws, and giving.</p>
      <form onSubmit={submit} className="space-y-4">
        <input
          required placeholder="Username"
          className="w-full border border-ink/15 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-coral"
          value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })}
        />
        <input
          required type="password" placeholder="Password"
          className="w-full border border-ink/15 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-coral"
          value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        {error && <p className="text-coral text-sm">{error}</p>}
        <button className="w-full bg-ink text-paper py-3.5 rounded-xl font-semibold hover:bg-coral transition-colors">
          Sign in
        </button>
      </form>
      <p className="text-sm text-inkmuted mt-6">
        New here? <Link to="/signup" className="text-ink underline">Create an account</Link>
      </p>
    </div>
  );
}
