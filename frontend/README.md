# Digital Heroes — Frontend (React + Vite + Tailwind)

## Local setup
```
cd frontend
npm install
cp .env.example .env   # point VITE_API_URL at your backend
npm run dev
```

## Deploying to Vercel (new account)
1. Push this repo to GitHub.
2. In a **new** Vercel account: New Project → import the repo → set root directory to `frontend/`.
3. Framework preset: Vite. Build command `npm run build`, output dir `dist`.
4. Add env var `VITE_API_URL` = your deployed backend URL + `/api` (e.g. `https://digital-heroes-api.onrender.com/api`).
5. Deploy. Vercel gives you the live URL required for submission.
