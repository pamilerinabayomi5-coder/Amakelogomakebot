# 📊 Telegram Word Counter Bot

A Telegram bot that counts words, characters, sentences, paragraphs, and shows the top 5 most-used words — hosted on Railway.

---

## Features

| Feature | Details |
|---|---|
| Word count | Total and unique |
| Character count | With and without spaces |
| Sentence & paragraph count | Auto-detected |
| Top 5 words | Most frequent words |
| Avg word length | Across the whole text |
| File support | Upload `.txt` files |
| Reply mode | `/count` on any message |

---

## Commands

| Command | Action |
|---|---|
| `/start` | Welcome message |
| `/help` | Usage tips |
| `/count` | Count words in the replied-to message |
| _(any text)_ | Count words in the message |
| _(attach .txt)_ | Count words in the file |

---

## Local Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd telegram-word-counter-bot

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your bot token
export BOT_TOKEN="your-token-here"   # Windows: set BOT_TOKEN=your-token-here

# 5. Run
python bot.py
```

---

## Deploy to Railway

### Step 1 — Create your Telegram bot
1. Open Telegram and message **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the **API token** you receive

### Step 2 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

### Step 3 — Deploy on Railway
1. Go to [railway.app](https://railway.app) and sign in
2. Click **New Project → Deploy from GitHub repo**
3. Select your repository
4. Go to **Variables** and add:
   ```
   BOT_TOKEN = <your telegram bot token>
   ```
5. Railway will automatically detect the `Procfile` / `railway.toml` and deploy

### Step 4 — Verify
- Railway will show **Active** in the deployment logs
- Message your bot on Telegram — it should respond instantly

---

## Project Structure

```
telegram-word-counter-bot/
├── bot.py            # Main bot logic
├── requirements.txt  # Python dependencies
├── Procfile          # Process definition for Railway
├── railway.toml      # Railway build & deploy config
├── .gitignore
└── README.md
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `BOT_TOKEN` | ✅ | Your Telegram bot token from @BotFather |
