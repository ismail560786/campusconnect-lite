# CampusConnect Lite 🎓
### AI Study & Resource Hub for Students — No Database Needed

A simple, beginner-friendly hub where students can search academic
resources (notes, past papers, slides, assignments), find study groups,
and ask an AI assistant for study help — all built with plain CSV files
instead of a database.

**Team:** Ismail (MBA, Team Leader) · Kashif (BS IT, Technical Lead) ·
Hafsa (Professor, Engineering, Academic Lead) · Ifra (BS English, Content & UX Lead)

---

## 1. What's in this folder

```
campusconnect-lite/
├── app.py              → the Streamlit app (4 tabs)
├── resources.csv        → sample academic resources data
├── study_groups.csv     → sample study group data
├── requirements.txt     → Python packages needed
├── .env.example         → template for your API key (copy to .env)
├── .gitignore            → keeps your real API key out of GitHub
└── README.md             → this file
```

## 2. What the app does (no SQL, no database — just CSV + pandas)

| Tab | What it does | Uses AI? |
|---|---|---|
| 📚 Resources | Search/filter notes, past papers, slides, assignments by subject, type, semester, keyword | No |
| 👥 Study Groups | Search/filter study groups by subject, day, mode | No |
| 🤖 AI Study Assistant | Ask for explanations, study plans, revision points, practice questions | Yes (Gemini API) |
| ℹ️ About | Project & team info | No |

---

## 3. Run it on your own laptop first

### Step 1 — Get a free Gemini API key
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with a Google account
3. Click "Create API Key" and copy it

### Step 2 — Set up the project
```bash
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3 — Add your API key
```bash
cp .env.example .env
```
Open `.env` and paste your real key:
```
GOOGLE_API_KEY=AIza...your real key here...
```

### Step 4 — Run the app
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`. Test all 4 tabs.

---

## 4. Push the code to GitHub (Kashif does this — no terminal needed)

**Easiest way (recommended for beginners):**
1. Go to https://github.com and sign in (or create a free account)
2. Click **"+"** (top-right) → **"New repository"**
3. Name it `campusconnect-lite`, keep it **Public**, click **"Create repository"**
4. Click **"Add file" → "Upload files"**
5. Drag in: `app.py`, `resources.csv`, `study_groups.csv`, `requirements.txt`, `.gitignore`, `README.md`
   (Do NOT upload `.env` — only `.env.example` is safe to upload)
6. Scroll down, click **"Commit changes"**

This page's URL is your **Code Link**.

**Add teammates as collaborators:** Repo → Settings → Collaborators → Add people.

---

## 5. Deploy for free on Streamlit Community Cloud

1. Go to https://share.streamlit.io and sign in with GitHub
2. Click **"New app"**
3. Select repo `campusconnect-lite`, branch `main`, file `app.py`
4. Click **"Advanced settings" → Secrets**, add:
   ```
   GOOGLE_API_KEY = "your_real_key_here"
   ```
5. Click **"Deploy"**. Wait 1–2 minutes.
6. You'll get a public URL like:
   `https://campusconnect-lite-yourname.streamlit.app`

This is your **Deployment/App Link**.

### If deployment fails
- Check the "Manage app" logs on Streamlit Cloud for the exact error
- Most common cause: a typo in `requirements.txt` or a missing Secret — re-check Step 4 above
- Make sure `resources.csv` and `study_groups.csv` were uploaded to GitHub (the app needs them)

### To update the app later
Just upload the changed file again on GitHub (Step 4) — Streamlit Cloud automatically redeploys within a minute or two.

---

## 6. Pre-recording checklist

- [ ] App loads on the public link with no errors
- [ ] Resources tab shows results for at least one subject
- [ ] Study Groups tab shows at least one match
- [ ] AI Study Assistant answers a real question
- [ ] About tab shows all 4 team members

---

## 7. Where each team member's work shows up

| Area | Owner |
|---|---|
| App code, all 4 tabs, API integration, deployment | Kashif |
| Sample data accuracy, academic realism, testing from a faculty/student view | Hafsa |
| AI prompt wording, tab labels, button text, README clarity | Ifra |
| Problem framing, PRD coordination, final submission | Ismail |
