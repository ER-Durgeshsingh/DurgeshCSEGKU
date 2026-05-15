# CSEClass AI Attendance - Setup & Live Deployment Guide

## 1. Supabase setup
1. Open Supabase Dashboard.
2. Create a new project.
3. Go to **SQL Editor**.
4. Open `supabase/schema.sql` from this project.
5. Copy all SQL and click **Run**.
6. Go to **Project Settings > API**.
7. Copy `Project URL` and `anon public key`.
8. Paste them in `.streamlit/secrets.toml`.

## 2. Gmail OTP setup
1. Open your Google Account.
2. Enable 2-Step Verification.
3. Search **App Passwords**.
4. Create an app password for Mail.
5. Paste Gmail and app password in `.streamlit/secrets.toml`:

```toml
GMAIL_ADDRESS = "yourgmail@gmail.com"
GMAIL_APP_PASSWORD = "your16digitapppassword"
```

If Gmail is not configured, OTP still works in local development by showing a DEV OTP warning on screen.

## 3. Run locally in VS Code
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 4. Deploy on Streamlit Cloud
1. Push project to GitHub.
2. Open Streamlit Cloud.
3. New app > select GitHub repository.
4. Main file path: `app.py`.
5. In Streamlit Cloud app settings > Secrets, paste:

```toml
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_anon_key"
GMAIL_ADDRESS = "yourgmail@gmail.com"
GMAIL_APP_PASSWORD = "your_app_password"
```

6. Deploy.

## 5. New features added
- Supabase SQL setup file.
- Teacher registration with Gmail/email.
- Gmail OTP login.
- Forgot password with Gmail OTP.
- Attendance Excel export.
- Monthly register-style Excel export with day-wise P/A marking.
- University Roll Number in student registration, PDF and Excel.
- Monthly attendance PDF export.
- Admin dashboard.
- Auto attendance analytics.
- Low attendance alerts below 75%.
- Month-wise attendance trend.
