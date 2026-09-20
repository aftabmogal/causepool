import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";

export default function Signup() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const { data } = await api.post("/auth/signup/", form);
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      navigate("/subscribe");
    } catch (err) {
      setError(err.response?.data?.username?.[0] || err.response?.data?.password?.[0] || "Signup failed. Try a different username.");
    }
  };

  return (
    <div className="max-w-md mx-auto px-6 py-20">
      <h1 className="font-display text-3xl text-ink mb-2">Create your account</h1>
      <p className="text-inkmuted mb-8">Takes under a minute. No golf clubhouse required.</p>
      <form onSubmit={submit} className="space-y-4">
        <input
          required placeholder="Username"
          className="w-full border border-ink/15 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-coral"
          value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })}
        />
        <input
          required type="email" placeholder="Email"
          className="w-full border border-ink/15 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-coral"
          value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          required type="password" placeholder="Password (min. 8 characters)"
          className="w-full border border-ink/15 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-coral"
          value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        {error && <p className="text-coral text-sm">{error}</p>}
        <button className="w-full bg-ink text-paper py-3.5 rounded-xl font-semibold hover:bg-coral transition-colors">
          Create account
        </button>
      </form>
      <p className="text-sm text-inkmuted mt-6">
        Already have an account? <Link to="/login" className="text-ink underline">Sign in</Link>
      </p>
    </div>
  );
}
