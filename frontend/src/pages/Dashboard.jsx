import { useEffect, useState } from "react";
import api from "../api";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [scoreForm, setScoreForm] = useState({ value: "", date: "" });
  const [error, setError] = useState("");

  const load = () => api.get("/dashboard/me/").then((res) => setData(res.data));

  useEffect(() => { load(); }, []);

  const addScore = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.post("/scores/", { value: Number(scoreForm.value), date: scoreForm.date });
      setScoreForm({ value: "", date: "" });
      load();
    } catch (err) {
      setError(err.response?.data?.non_field_errors?.[0] || err.response?.data?.value?.[0] || "Couldn't save that score.");
    }
  };

  if (!data) return <div className="max-w-5xl mx-auto px-6 py-16 text-inkmuted">Loading your dashboard…</div>;

  const { subscription, scores, participation, winnings } = data;

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <h1 className="font-display text-4xl text-ink mb-10">Your dashboard</h1>

      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <StatCard label="Subscription" value={subscription.status} sub={subscription.plan ? `${subscription.plan} plan` : "Not subscribed"} />
        <StatCard label="Supporting" value={subscription.charity || "—"} sub={subscription.charity_percentage ? `${subscription.charity_percentage}% of your fee` : ""} />
        <StatCard label="Total won" value={`₹${winnings.total_won}`} sub={`₹${winnings.pending} pending payout`} />
      </div>

      <div className="grid md:grid-cols-2 gap-10">
        <section>
          <h2 className="font-display text-2xl text-ink mb-4">Your last 5 scores</h2>
          <p className="text-sm text-inkmuted mb-4">These double as your numbers in the monthly draw — Stableford, 1 to 45.</p>
          <ul className="space-y-2 mb-6">
            {scores.length === 0 && <li className="text-inkmuted text-sm">No scores yet — add your first round below.</li>}
            {scores.map((s) => (
              <li key={s.date} className="flex items-center justify-between bg-white/60 border border-ink/10 rounded-xl px-4 py-3">
                <span className="text-inkmuted text-sm">{s.date}</span>
                <span className="font-display text-lg text-ink">{s.value}</span>
              </li>
            ))}
          </ul>
          <form onSubmit={addScore} className="flex gap-3">
            <input type="date" required value={scoreForm.date}
              onChange={(e) => setScoreForm({ ...scoreForm, date: e.target.value })}
              className="border border-ink/15 rounded-xl px-3 py-2 flex-1 focus:outline-none focus:ring-2 focus:ring-coral" />
            <input type="number" min="1" max="45" required placeholder="Score" value={scoreForm.value}
              onChange={(e) => setScoreForm({ ...scoreForm, value: e.target.value })}
              className="border border-ink/15 rounded-xl px-3 py-2 w-24 focus:outline-none focus:ring-2 focus:ring-coral" />
            <button className="bg-ink text-paper px-5 rounded-xl font-semibold hover:bg-coral transition-colors">Add</button>
          </form>
          {error && <p className="text-coral text-sm mt-2">{error}</p>}
        </section>

        <section>
          <h2 className="font-display text-2xl text-ink mb-4">Participation & winnings</h2>
          <div className="bg-white/60 border border-ink/10 rounded-2xl p-6 mb-6">
            <p className="text-sm text-inkmuted mb-1">Draws entered</p>
            <p className="font-display text-2xl text-ink mb-4">{participation.draws_entered}</p>
            <p className="text-sm text-inkmuted mb-1">Next draw</p>
            <p className="font-display text-lg text-ink">{participation.next_draw_month || "Not yet scheduled"}</p>
          </div>

          <div className="space-y-3">
            {winnings.records.length === 0 && (
              <p className="text-sm text-inkmuted">No wins yet — every subscriber's scores are entered automatically each month.</p>
            )}
            {winnings.records.map((w, i) => (
              <div key={i} className="flex items-center justify-between bg-white/60 border border-ink/10 rounded-xl px-4 py-3">
                <div>
                  <p className="text-sm text-ink font-medium">{w.match_type}-number match</p>
                  <p className="text-xs text-inkmuted">{w.draw_month}</p>
                </div>
                <div className="text-right">
                  <p className="font-display text-ink">₹{w.amount}</p>
                  <p className="text-xs text-inkmuted capitalize">{w.status}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

function StatCard({ label, value, sub }) {
  return (
    <div className="bg-white/60 border border-ink/10 rounded-2xl p-6">
      <p className="text-xs uppercase tracking-widest text-gold font-semibold mb-2">{label}</p>
      <p className="font-display text-2xl text-ink capitalize">{value}</p>
      {sub && <p className="text-sm text-inkmuted mt-1">{sub}</p>}
    </div>
  );
}
