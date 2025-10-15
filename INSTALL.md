# NutriGuard — Installation & Setup

This document walks through a full local setup for the NutriGuard Django project on Windows (PowerShell). It covers both pipenv and plain venv workflows, database setup, environment variables, migrations, media/static handling, and common troubleshooting steps.

## Prerequisites
- Python 3.11+ (project was developed with Python 3.12). Verify with:

```pwsh
python --version
```

- Git (optional, to clone repository)
- PostgreSQL (recommended) or you can use the included `db.sqlite3` for quick testing
- Optional: `pipenv` (recommended) or use `venv` + `pip`
- (Optional) Pillow and requests if not already in your environment — used for image handling

## 1) Clone repository (or use your local copy)

```pwsh
# clone (if needed)
git clone <repo-url>
cd Capstone-Project
```

You should be in the project root that contains `manage.py`.

## 2) Install dependencies

This project contains a `Pipfile`. Use either pipenv or a virtualenv.

### Option A — pipenv (recommended)

```pwsh
# install pipenv if you don't have it
pip install pipenv

# create virtualenv and install dependencies from Pipfile
pipenv install

# activate the environment for running commands interactively
pipenv shell
```

When in `pipenv shell`, you can use `python` and `pip` normally.

### Option B — venv + pip

```pwsh
python -m venv .venv
# PowerShell: activate
.\.venv\Scripts\Activate.ps1
# then install packages (if you have a requirements.txt)
# or reproduce Pipfile dependencies manually:
pip install django pillow requests python-dotenv psycopg2-binary
```

> Note: the project uses `python-dotenv` (dotenv.load_dotenv) to read `.env` automatically; keep this in mind when setting environment variables.

## 3) Configure environment variables

Create a `.env` file in the project root (next to `manage.py`) to store secrets and DB credentials. Example `.env`:

```
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Database (Postgres example)
DB_NAME=nutriguard
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# AI key used by utils.py (remove in production / store securely)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional email settings (in DEBUG email files are written)
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=secret
```

The project already uses `load_dotenv()` in settings so environment variables from `.env` will be read.

Important: the included `NutriGuard/settings.py` expects DB settings to be present directly in `DATABASES` unless you modify it. If you want to use environment variables for DB, update `settings.py` or pass them in the environment before running Django.

## 4) Database setup

### PostgreSQL (recommended)

1. Create a database and user (example using `psql`):

```pwsh
# open psql as postgres user
psql -U postgres

# inside psql:
CREATE DATABASE nutriguard;
-- create or set your user/password if needed
-- CREATE USER myuser WITH PASSWORD 'mypassword';
-- GRANT ALL PRIVILEGES ON DATABASE nutriguard TO myuser;
\q
```

2. Make sure the DB credentials in `settings.py` or your environment point to the DB you created.

### SQLite (quick testing)

The repo already contains `db.sqlite3`. For a clean run you can remove it and let Django create one.

## 5) Migrations

Run Django migrations to create tables:

```pwsh
# If using pipenv
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate

# or if in an activated venv
python manage.py makemigrations
python manage.py migrate
```

> If you see errors about missing relations (e.g. `main_app_allergy_food`), check `python manage.py showmigrations main_app` to see applied migrations and re-run `migrate`. If migrations were faked or the DB was restored from a dump, you may need to reapply or manually repair schema — ask me for help if that happens.

## 6) Create a superuser (optional)

```pwsh
pipenv run python manage.py createsuperuser
```

Follow the prompts to create an admin account.

## 7) Media directory (avatars & uploads)

Ensure the `media/` directory exists and is writable. On Windows PowerShell:

```pwsh
# create a media folder in project root
New-Item -ItemType Directory -Path .\media
```

When `DEBUG = True`, `NutriGuard/urls.py` is configured to serve `MEDIA_URL` from `MEDIA_ROOT`.

## 8) Running the development server

```pwsh
# pipenv
pipenv run python manage.py runserver

# or inside activated venv
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser. Log in or sign up. After sign-in you will be redirected to `/home/` (the dashboard).

## 9) AI image/text generation

The project uses Google GenAI client and an external image service in `main_app/utils.py`. To allow AI calls:

- Set `GEMINI_API_KEY` in your `.env` (or environment) before running server.
- If you don't have an API key or want to disable AI during development, you can stub out calls in `main_app/utils.py` (return sample data) or remove the lines that set `os.environ`.

## 10) Email (password reset)

- In DEBUG the project uses `filebased.EmailBackend` and writes message files to `sent_emails/`. Check that directory for reset link emails.

## 11) Optional: Pillow & Image libraries

If you plan to rely on image generation or user-uploaded avatars, be sure Pillow is installed:

```pwsh
pipenv run pip install pillow
```

## 12) Collect static (production)

For production, run:

```pwsh
pipenv run python manage.py collectstatic
```

Then configure a proper static/media server (nginx, S3, etc.). Do not serve uploaded media from Django in production.

## Troubleshooting

- Template errors on login or chat:
  - Ensure you are running the server with the same Python environment where dependencies were installed.

- ProgrammingError: relation "main_app_allergy_food" does not exist
  - This indicates the many-to-many join table is missing in the DB. Try re-running migrations:

```pwsh
pipenv run python manage.py showmigrations main_app
pipenv run python manage.py migrate
```

  - If `showmigrations` shows migrations applied but the table is missing, inspect your migration files in `main_app/migrations/` and consult your DB dump history. I can help repair specific cases if you share the migration output and error.

- Avatars not visible after upload
  - Ensure `MEDIA_ROOT` exists and the `media/` folder is writable.
  - Check the uploaded file path in the `media/` folder and confirm the URL under `/media/` is reachable in the browser.

- AI calls failing or no images
  - Ensure `GEMINI_API_KEY` is set and valid. The image generator uses external services and may fail silently; check server logs for exceptions.

## Deployment hints (brief)
- Use environment variables (not `.env`) in production for secret keys and DB credentials.
- Serve media and static via a dedicated server (nginx) or cloud storage (S3).
- Use a WSGI server (gunicorn/uvicorn) and process manager (systemd) behind nginx.

## Quick checklist (copy/paste)

```pwsh
# optional: pipenv workflow
pip install pipenv
pipenv install
pipenv shell
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser
New-Item -ItemType Directory -Path .\media
pipenv run python manage.py runserver
```

If you want, I can:
- Add a one-click PowerShell script (`setup.ps1`) to automate the steps above.
- Add a `requirements.txt` if you prefer a `pip` workflow.
- Add server-side image resizing/validation (Pillow) and demos.

---

If anything fails for you specifically, paste the console error here and I will diagnose the next steps.