import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function Subscribe() {
  const [charities, setCharities] = useState([]);
  const [plan, setPlan] = useState("monthly");
  const [charityId, setCharityId] = useState("");
  const [pct, setPct] = useState(10);
  const [status, setStatus] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/charities/").then((res) => {
      setCharities(res.data);
      if (res.data.length) setCharityId(res.data[0].id);
    });
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    setStatus("Processing…");
    try {
      const { data } = await api.post("/subscriptions/checkout/", {
        plan, charity_id: charityId, charity_percentage: pct,
      });
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        setStatus(data.detail || "Subscribed.");
        setTimeout(() => navigate("/dashboard"), 900);
      }
    } catch {
      setStatus("Something went wrong — please sign in and try again.");
    }
  };

  return (
    <div className="max-w-xl mx-auto px-6 py-16">
      <h1 className="font-display text-4xl text-ink mb-2">Set up your subscription</h1>
      <p className="text-inkmuted mb-10">Pick a plan, choose your cause, decide how much of it wins.</p>

      <form onSubmit={submit} className="space-y-8">
        <div>
          <p className="font-semibold text-ink mb-3">Plan</p>
          <div className="grid grid-cols-2 gap-4">
            {["monthly", "yearly"].map((p) => (
              <button type="button" key={p} onClick={() => setPlan(p)}
                className={`rounded-xl border-2 px-5 py-4 text-left transition-colors ${
                  plan === p ? "border-coral bg-coral/5" : "border-ink/10"
                }`}>
                <p className="font-display text-lg capitalize text-ink">{p}</p>
                <p className="text-sm text-inkmuted">{p === "yearly" ? "Best value — two months free" : "Cancel anytime"}</p>
              </button>
            ))}
          </div>
        </div>

        <div>
          <p className="font-semibold text-ink mb-3">Your charity</p>
          <select value={charityId} onChange={(e) => setCharityId(e.target.value)}
            className="w-full border border-ink/15 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-coral">
            {charities.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>

        <div>
          <div className="flex justify-between mb-2">
            <p className="font-semibold text-ink">Contribution share</p>
            <p className="font-display text-coral">{pct}%</p>
          </div>
          <input type="range" min="10" max="100" value={pct} onChange={(e) => setPct(Number(e.target.value))}
            className="w-full accent-coral" />
          <p className="text-xs text-inkmuted mt-1">Minimum 10% — raise it any time, permanently or just this cycle.</p>
        </div>

        <button className="w-full bg-ink text-paper py-3.5 rounded-xl font-semibold hover:bg-coral transition-colors">
          Confirm & subscribe
        </button>
        {status && <p className="text-sm text-inkmuted text-center">{status}</p>}
      </form>
    </div>
  );
}
