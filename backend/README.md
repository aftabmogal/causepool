# Digital Heroes — Backend (Django + DRF)

## Local setup
```
cd backend
python -3.12 -m venv venv && source venv/scripts/activate
pip install -r requirements.txt
cp .env.example .env   # fill in real values
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_charities
python manage.py runserver
```

## Troubleshooting: pip fails to build psycopg2-binary / Pillow on Windows
If `pip install -r requirements.txt` fails with `Microsoft Visual C++ 14.0 or greater is required` or `RequiredDependencyException: zlib`, it's because your Python version is newer than what those pinned packages had prebuilt wheels for — pip falls back to compiling from source, which needs build tools you don't have. Two ways to fix it, either works:
- **Just re-run `pip install -r requirements.txt`** — this repo now pins `psycopg2-binary>=2.9.11` and `Pillow>=11.0`, both of which ship prebuilt Windows wheels for Python 3.13/3.14. No compiler needed.
- If you still hit build errors on a very new Python version, use Python 3.12 for this project instead (`py -3.12 -m venv venv`) — it has the widest wheel support across the whole ecosystem, not just these two packages.

## Deploying (Render + Supabase, both NEW accounts)
1. Create a new Supabase project → copy the Postgres connection string (Session pooler, port 5432 or 6543) into `DATABASE_URL`.
2. Create a new Render account → New Web Service → connect this repo's `backend/` folder.
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start command: `gunicorn config.wsgi:application`
   - Add all `.env` vars in Render's Environment tab.
3. After first deploy, run once from Render's shell: `python manage.py createsuperuser` and `python manage.py seed_charities`.
4. Set `CORS_ALLOWED_ORIGINS` and `FRONTEND_URL` to your Vercel frontend URL once deployed.
5. Stripe: use **test mode** keys only. Create two test Products/Prices (monthly, yearly) in the Stripe dashboard, put their price IDs in `STRIPE_PRICE_MONTHLY` / `STRIPE_PRICE_YEARLY`. Add a webhook endpoint pointing at `https://<your-backend>/api/subscriptions/webhook/` listening for `checkout.session.completed` and `customer.subscription.deleted`.
   - If you skip Stripe entirely, checkout still works via a dev-mode fallback that activates the subscription locally — good enough for demoing every other module before your deadline.

## Running the monthly draw
```
python manage.py run_draw --method weighted   # or --method random
```
This only **simulates** a draw (creates an unpublished DrawResult). Go to `/admin/draws/drawresult/`, select it, and run the **"Publish selected draw(s)"** admin action — this computes 3/4/5-number matches against every active subscriber's 5 stored scores, splits the prize pool by tier (40/35/25%), rolls over an unclaimed jackpot, and creates Winner records.

## Design note (ambiguity resolved)
The PRD doesn't explicitly say how the draw picks winners from subscribers. We treat each user's 5 stored Stableford scores (range 1–45) as their "lottery numbers" and match them against 5 numbers drawn monthly — this is what connects the score-entry system to the draw/prize system, and is the only reading of the PRD where both systems interact.

## Admin dashboard
Rather than building a bespoke admin UI (not enough time to do well in 2 days), this uses a heavily customized Django Admin (`/admin/`) as the admin dashboard:
- User & subscription management (built-in)
- Charity + event management with inline editing
- Draw simulation (management command) + one-click publish/compute-winners action
- Winner verification + mark-as-paid actions
- `/api/dashboard/admin-analytics/` gives raw numbers if you want to build a small analytics widget on the frontend later
