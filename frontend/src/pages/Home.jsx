import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <div className="relative overflow-hidden">
      <div className="blob w-96 h-96 bg-gold -top-20 -right-20" />
      <div className="blob w-80 h-80 bg-coral top-96 -left-32" />

      <section className="relative max-w-6xl mx-auto px-6 pt-16 pb-24 grid md:grid-cols-[1.2fr_1fr] gap-12 items-center">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        >
          <p className="text-inkmuted font-medium mb-4">Play your round. Fund a cause. Win together.</p>
          <h1 className="font-display text-5xl md:text-6xl leading-[1.05] text-ink mb-6">
            Every score you post
            <br />
            <span className="text-coral">moves someone else's life forward.</span>
          </h1>
          <p className="text-lg text-inkmuted max-w-md mb-8">
            Log your last five rounds, back a charity you believe in, and get entered
            into a monthly prize draw built from the community's own play.
          </p>
          <div className="flex items-center gap-4">
            <Link to="/signup" className="bg-coral text-white px-7 py-3.5 rounded-full font-semibold hover:bg-ink transition-colors">
              Start your streak
            </Link>
            <Link to="/charities" className="text-ink font-semibold underline decoration-gold decoration-2 underline-offset-4">
              See the causes
            </Link>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.94 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, ease: "easeOut", delay: 0.15 }}
          className="bg-ink text-paper rounded-[2rem] p-8 shadow-xl"
        >
          <p className="text-xs uppercase tracking-widest text-gold mb-3">This month's draw</p>
          <div className="flex gap-3 mb-6">
            {[7, 14, 22, 31, 40].map((n) => (
              <div key={n} className="w-11 h-11 rounded-full bg-paper text-ink font-display font-semibold flex items-center justify-center">
                {n}
              </div>
            ))}
          </div>
          <p className="text-sm text-paper/70 leading-relaxed">
            Your last five Stableford scores double as your numbers. Match three,
            four, or all five in the monthly draw to win a share of the pool —
            funded entirely by the community's subscriptions.
          </p>
        </motion.div>
      </section>

      <section className="relative bg-ink text-paper py-20">
        <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-3 gap-10">
          {[
            { label: "Score", body: "Enter your last five rounds. We keep the most recent five, always." },
            { label: "Give", body: "At least 10% of your subscription goes straight to a charity you choose." },
            { label: "Win", body: "Match your scores against the monthly draw for a share of the prize pool." },
          ].map((item) => (
            <div key={item.label}>
              <h3 className="font-display text-2xl mb-2 text-gold">{item.label}</h3>
              <p className="text-paper/75 leading-relaxed">{item.body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="relative max-w-6xl mx-auto px-6 py-20 text-center">
        <h2 className="font-display text-3xl md:text-4xl text-ink mb-4">
          The causes come first. The game is how we fund them.
        </h2>
        <p className="text-inkmuted max-w-xl mx-auto mb-8">
          Browse the charities our community already supports, or bring your own.
        </p>
        <Link to="/charities" className="inline-block bg-ink text-paper px-7 py-3.5 rounded-full font-semibold hover:bg-coral transition-colors">
          Browse charities
        </Link>
      </section>
    </div>
  );
}
