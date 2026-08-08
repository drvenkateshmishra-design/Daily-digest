# Daily Digest — setup guide

What this does: every day, a script runs automatically on GitHub's servers (free),
pulls recent news + PubMed journal articles, builds a formatted PDF, and sends it
to you on Telegram via a bot. No computer of yours needs to be on, and nothing
here costs money.

Follow these steps in order. Don't skip ahead.

---

## Step 1 — Create the repo (done — you already have `Daily-digest`)

Just make sure every file from this project is uploaded, including the
`.github/workflows/daily-digest.yml` file (this is what we just fixed together).

## Step 2 — Create your Telegram bot

1. Open Telegram (app or web).
2. Search for **@BotFather** (this is Telegram's official bot for creating bots
   — verified blue checkmark).
3. Send it: `/newbot`
4. It'll ask for a name (anything, e.g. "Venki Daily Digest") and a username
   (must end in `bot`, e.g. `venki_digest_bot`).
5. BotFather replies with a **token** — a long string like
   `123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`. Copy it somewhere safe.

## Step 3 — Get your chat ID

1. Search for your new bot by its username (from Step 2) in Telegram and open
   a chat with it.
2. Send it any message, e.g. "hi".
3. In your browser, go to this URL, replacing `<TOKEN>` with your actual token
   from Step 2:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. You'll see some JSON text. Look for `"chat":{"id":` — the number right after
   that is your **chat ID** (looks like `987654321`). Copy it.

   If you see an empty response `{"ok":true,"result":[]}`, you sent the message
   before opening this URL — go send "hi" to the bot again, then reload this
   URL.

## Step 4 — Add secrets to GitHub

1. In your repo: **Settings → Secrets and variables → Actions**.
2. Click **New repository secret**, add each of these:

| Name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | the token from Step 2 |
| `TELEGRAM_CHAT_ID` | the number from Step 3 |

(If `TWILIO_...` secrets exist from before, you can delete those — no longer
used.)

## Step 5 — Test it manually

1. Go to the **Actions** tab in your repo.
2. Click **Daily Digest** (left sidebar) → **Run workflow** button → **Run workflow**.
3. Click into the run, watch the steps. Takes about a minute.
4. If it goes green, check Telegram — the PDF should arrive within seconds.
5. If a step fails (red X), click it to see the error, and send it to me.

## Step 6 — Let it run itself

Once Step 5 works, you're done. It runs automatically every day at 06:30 IST.

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

Ping me once you've done Steps 2–5, or if anything errors out.
