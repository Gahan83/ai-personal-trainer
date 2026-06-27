# AI Personal Trainer

An always-on, personalized AI gym & fitness coach built to the PRD for **Gahan**
— 4× gym/week, 1× football, 2 rest days, and a set of hard training constraints
the agent never violates.

It is a *proactive agent*, not just a plan generator: it suggests the day's
workout, adapts to a 30-second readiness check-in, tracks lifts and surfaces
PRs/plateaus, gives conversational guidance, and nudges nutrition/recovery.

## Hard constraints (enforced in code, not just prompts)

1. **No abs/core work — ever** (warm-ups, finishers, or any suggestion).
2. **Football is a training day** — never a gym session the same day.
3. At least **one full rest day between back-to-back hard sessions**.
4. **No leg day the day before football.**
5. All programming is **non-competitive** — physique, strength, longevity.

> Note: the PRD's illustrative split placed legs the day before football, which
> violates constraint #4. The default split shifts legs to Tuesday so it is
> constraint-clean: `push · legs · rest · pull · football · upper · rest`.

These live in [`backend/app/services/trainer.py`](backend/app/services/trainer.py)
and are validated on every plan, every logged set, and every AI response.

## Feature → version map (from the PRD)

| Feature | Version | Where |
|---|---|---|
| Daily workout suggestion | V1 | `GET /agent/today` |
| Conversational guidance | V1 | `POST /agent/chat` |
| Progress tracking (PRs, volume, plateaus) | V1 | `GET /workouts/progress` |
| Football-day awareness | V1 | planner in `trainer.py` |
| Adaptive recovery engine (check-in) | V2 | `POST /checkin/` → reshapes `/agent/today` |
| Nutrition & hydration nudges | V2 | `/nutrition/*` |
| Wearable / health data sync | V3 | `/wearables/*` (manual ingest + recovery score) |

## Tech stack

- **Backend:** FastAPI · SQLAlchemy · SQLite · Azure OpenAI (`openai` SDK)
- **Frontend:** React 18 · React Router · styled-components · axios · react-hot-toast

## Architecture

```
backend/app/
  core/config.py        # settings (Azure OpenAI env vars)
  core/database.py      # SQLAlchemy engine/session
  core/seed.py          # create tables + seed the Gahan user
  models/models.py      # User, WorkoutSession, SetLog, CheckIn, NutritionLog, WearableData
  services/trainer.py   # split, no-abs exercise library, constraint engine, adaptive planner
  services/ai_service.py# Azure OpenAI wrapper (graceful no-op without keys)
  api/endpoints/        # agent, workouts, checkin, nutrition, wearables, users, exercises, mcp

frontend/src/pages/     # Dashboard (Today), Coach (chat), Progress, Nutrition, Recovery, Profile
```

The app is **single-user** (Gahan = user id 1, seeded on startup). It runs fully
offline using the deterministic planner; adding Azure OpenAI keys turns on the
AI coach note and the conversational `/coach` chat.

## Getting started

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env             # then fill in Azure OpenAI values (see below)
uvicorn app.main:app --reload
```

API at `http://localhost:8000` · docs at `http://localhost:8000/docs`.
The SQLite DB (`ai_trainer.db`) and Gahan user are created automatically.

### 2. Azure OpenAI config (`backend/.env`)

`.env` is git-ignored. Fill these:

```
OPENAI_API_KEY=<your-azure-openai-key>
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_API_VERSION=2024-06-01
CHAT_MODEL=<your-deployment-name>     # e.g. gpt-4o-mini
```

Without these, workout planning still works; only AI chat/coaching notes are off.

### 3. Frontend

```bash
cd frontend
npm install
npm start                       # http://localhost:3000
```

## Key endpoints

```
GET  /api/v1/agent/today          # adaptive workout for today
GET  /api/v1/agent/week           # weekly split + constraint check
POST /api/v1/agent/chat           # conversational coach
POST /api/v1/checkin/             # readiness check-in (soreness/energy)
POST /api/v1/workouts/{id}/complete
POST /api/v1/workouts/{id}/sets   # log a set (rejects abs exercises)
GET  /api/v1/workouts/progress    # PRs, volume, plateau alerts
GET  /api/v1/nutrition/nudges
POST /api/v1/wearables/sync
```

## License

MIT.
