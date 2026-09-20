# Digital Heroes — Submission

Full-stack app for the Digital Heroes PRD (Level 1): golf-score-driven charity
draw platform. Backend: Django + DRF. Frontend: React + Vite + Tailwind.
DB: Postgres (Supabase). Payments: Stripe (test mode) with a dev-mode fallback.

- `backend/` — API, auth, Stripe checkout, draw engine, Django Admin as the
  admin dashboard. See `backend/README.md` for setup + deploy steps.
- `frontend/` — public site, signup/login, charity directory, subscribe flow,
  user dashboard. See `frontend/README.md` for setup + deploy steps.

## 2-day build & submission plan

**Today**
1. `cd backend`, follow `backend/README.md` local setup, confirm signup/login/
   scores/charities/checkout/dashboard all work on `localhost` (they do out of
   the box with SQLite — no Supabase needed yet to develop).
2. Create your **new** Supabase project and **new** Render account. Point
   `DATABASE_URL` at Supabase, deploy backend to Render.
3. Create your **new** Vercel account, deploy `frontend/` pointed at the
   Render backend URL.
4. Run `python manage.py createsuperuser` and `seed_charities` on the deployed
   backend (via Render's shell).

**Tomorrow**
5. Walk the whole flow live: signup → subscribe → charity → add 5 scores →
   `python manage.py run_draw --method weighted` → publish in `/admin/` →
   confirm winnings show up on the dashboard.
6. Polish: add 2-3 more charities with images, double-check mobile layout,
   write the submission doc (live URL, test user creds, admin creds, this
   README as your architecture writeup).
7. Submit before the 22 Sept deadline.

## What's already handled for the evaluation criteria
- **Requirements interpretation**: every PRD section (§04–§11) maps to a
  Django app; the score↔draw connection ambiguity is resolved and documented
  in `backend/README.md`.
- **System design**: normalized models, JWT auth, Stripe webhook for real
  subscription lifecycle, rolling-5 score logic enforced server-side.
- **Data handling**: score validation (1–45, one per date, oldest auto-evicted),
  atomic prize-pool math with jackpot rollover.
- **Scalability**: apps are cleanly separated (accounts/charities/
  subscriptions/scores/draws/dashboard) so each can grow independently; the
  draw algorithm is swappable (`--method random|weighted`).
- **UI/UX**: no fairways, no plaid — a charity-first, editorial look (see
  `frontend/README.md` for local dev).
