# Daily Digest — setup guide

What this does: every day, a script runs automatically on GitHub's servers (free),
pulls recent news + PubMed journal articles, builds a formatted PDF, and sends it
to your WhatsApp via Twilio. No computer of yours needs to be on.

Follow these steps in order. Don't skip ahead.

---

## Step 1 — Create the repo

1. Log into GitHub.
2. Click the **+** (top right) → **New repository**.
3. Name it `daily-digest` (or anything). Set it to **Public** (required for free
   GitHub Pages, used in Step 2). Click **Create repository**.
4. On the new repo's page, click **Add file → Upload files**, and drag in
   *every file and folder* from this project (including the hidden `.github`
   folder — if your file browser hides it, use `git` instead, see note below).
5. Commit the upload (button at the bottom).

> **Note on the `.github` folder:** some file managers hide folders starting
> with a dot. If it doesn't appear when you drag files in, tell me and I'll
> give you the exact `git` commands instead — it's a two-minute fix.

## Step 2 — Enable GitHub Pages

This gives your PDF a public web address that Twilio can fetch from.

1. In your repo, go to **Settings → Pages**.
2. Under "Build and deployment", set **Source** to "Deploy from a branch".
3. Set **Branch** to `main`, folder to `/docs`. Click **Save**.
4. Wait a minute, then check the URL shown there — it'll look like
   `https://<your-username>.github.io/daily-digest/`. Keep this in mind for
   later; you don't need to do anything else with it now.

## Step 3 — Twilio account (this is what sends the WhatsApp message)

1. Go to twilio.com → sign up (free trial, no card needed to start).
2. Once in the Twilio Console (dashboard), find **Account SID** and
   **Auth Token** on the main page. Copy both somewhere safe — you'll paste
   them into GitHub in Step 4.
3. In the left sidebar: **Messaging → Try it out → Send a WhatsApp message**.
   This activates the Twilio Sandbox.
4. It'll show a phone number and a join code like `join happy-tiger`. From
   **your own WhatsApp**, send that exact message to that number. You'll get
   a confirmation reply — that links your WhatsApp to the sandbox.
5. Note your own WhatsApp number in international format, e.g. for India:
   `whatsapp:+9198XXXXXXXX` (no spaces, include the `+`). You'll need this
   in Step 4.

> ⚠️ **Known limitation:** WhatsApp only allows free automated messages within
> 24 hours of you last messaging the sandbox number. So the sandbox needs a
> "join"-style message from you roughly once a day for the automated send to
> keep working. For now: just re-send the join message if a digest doesn't
> arrive. Once the pipeline is running reliably, we can set up a proper
> approved WhatsApp template that removes this restriction entirely — that's
> a later step, not needed to get started.

## Step 4 — Add your secrets to GitHub

Secrets keep your credentials out of the code (never put them in config.py).

1. In your repo: **Settings → Secrets and variables → Actions**.
2. Click **New repository secret** and add each of these (one at a time):

| Name | Value |
|---|---|
| `TWILIO_ACCOUNT_SID` | from Step 3.2 |
| `TWILIO_AUTH_TOKEN` | from Step 3.2 |
| `TWILIO_WHATSAPP_TO` | your number from Step 3.5, e.g. `whatsapp:+9198XXXXXXXX` |

## Step 5 — Test it manually

Don't wait for the schedule — trigger it by hand first.

1. Go to the **Actions** tab in your repo.
2. Click **Daily Digest** (left sidebar) → **Run workflow** button → **Run workflow**.
3. Click into the run that appears, watch it go through each step. Takes
   1–3 minutes.
4. If every step gets a green check, check your WhatsApp — the PDF should
   arrive within a minute or two.
5. If a step fails (red X), click it to see the error, and send it to me —
   I'll tell you exactly what to fix.

## Step 6 — Let it run itself

Once Step 5 works, you're done. It'll now run automatically every day at
06:30 IST. Nothing more to do.

To change the time: open `.github/workflows/daily-digest.yml`, edit the
`cron:` line (it's in UTC — IST is UTC+5:30).

## Customizing what's in the digest

Everything you'd want to tweak day-to-day lives in **`config.py`**:
- `NEWS_FEEDS` — add/remove RSS feed URLs under each section
- `JOURNAL_SEARCHES` — the PubMed search terms per section
- `TIER1_JOURNALS` — journals that get starred and sorted to the top
- `PUBMED_LOOKBACK_DAYS`, `MAX_ARTICLES_PER_SECTION`, etc.

Edit the file on GitHub directly (pencil icon), commit — no need to touch
anything else.

## What's next (not needed yet)

- **Health data from your OnePlus Watch:** needs a small Tasker automation
  on your phone (Health Connect → webhook), since that data doesn't have a
  cloud API. We'll set this up once the above is running reliably.
- **Removing the 24-hour WhatsApp limitation:** via an approved message
  template, once you want this to be fully "set and forget."

Ping me once you've done Steps 1–5 and I'll help with whichever step is stuck,
or move on to the next phase.
