import { useEffect, useState } from "react";
import api from "../api";

export default function Charities() {
  const [charities, setCharities] = useState([]);
  const [q, setQ] = useState("");

  useEffect(() => {
    api.get(`/charities/${q ? `?search=${encodeURIComponent(q)}` : ""}`)
      .then((res) => setCharities(res.data))
      .catch(() => setCharities([]));
  }, [q]);

  const featured = charities.filter((c) => c.is_featured);
  const rest = charities.filter((c) => !c.is_featured);

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <h1 className="font-display text-4xl text-ink mb-2">Choose who your game supports</h1>
      <p className="text-inkmuted mb-8 max-w-lg">
        At least 10% of every subscription goes to the charity you pick. You can raise that share any time.
      </p>
      <input
        placeholder="Search charities…"
        value={q} onChange={(e) => setQ(e.target.value)}
        className="w-full max-w-sm border border-ink/15 rounded-xl px-4 py-3 mb-10 focus:outline-none focus:ring-2 focus:ring-coral"
      />

      {featured.length > 0 && (
        <div className="mb-12">
          <p className="text-xs uppercase tracking-widest text-gold font-semibold mb-4">Spotlighted this month</p>
          <div className="grid md:grid-cols-2 gap-6">
            {featured.map((c) => <CharityRow key={c.id} c={c} featured />)}
          </div>
        </div>
      )}

      <div className="divide-y divide-ink/10">
        {rest.map((c) => <CharityRow key={c.id} c={c} />)}
      </div>
    </div>
  );
}

function CharityRow({ c, featured }) {
  return (
    <div className={featured
      ? "bg-ink text-paper rounded-2xl p-6"
      : "py-6 flex items-start justify-between gap-6"}>
      <div>
        <h3 className={`font-display text-xl ${featured ? "text-gold" : "text-ink"}`}>{c.name}</h3>
        <p className={`text-sm mt-1 ${featured ? "text-paper/75" : "text-inkmuted"}`}>{c.tagline}</p>
        <p className={`text-sm mt-2 max-w-lg ${featured ? "text-paper/60" : "text-inkmuted"}`}>{c.description}</p>
        {c.events?.length > 0 && (
          <p className="text-xs mt-3 text-gold">Upcoming: {c.events[0].title} · {c.events[0].date}</p>
        )}
      </div>
    </div>
  );
}
