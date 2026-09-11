# GitHub Upload Guide - Latest Files

**Your GitHub:** `https://github.com/Baljinder95/fall-colors-data`

---

## 📦 4 Files to Upload

### 1. **index.html** (REPLACE existing)
- Source: `index_realtime.html`
- Where: Repo root
- What: Interactive map with live data
- Action: Edit existing file, paste entire content

### 2. **scraper.py** (NEW or REPLACE)
- Source: `scraper.py`
- Where: Repo root
- What: Extracts real-time data from Ontario Parks
- Action: Upload or overwrite

### 3. **.github/workflows/scrape.yml** (NEW)
- Source: `scrape.yml`
- Where: `.github/workflows/` folder (create if doesn't exist)
- What: GitHub Actions automation (runs scraper hourly)
- Action: Create new file in `.github/workflows/` folder

### 4. **parks_data.json** (KEEP or REPLACE)
- Source: `parks_data_realtime.json`
- Where: Repo root
- What: Live park data (auto-updated by scraper)
- Action: Rename to `parks_data.json` when uploading

---

## 🚀 Step-by-Step Upload

### Step 1: Replace `index.html`
```
1. Go to GitHub repo
2. Click "index.html"
3. Click pencil icon (edit)
4. Delete all content
5. Copy entire content from "index_realtime.html"
6. Paste it
7. Scroll down → "Commit changes"
```

### Step 2: Upload/Replace `scraper.py`
```
1. Go to GitHub repo root
2. Click "Add file" → "Upload files"
3. Select "scraper.py"
4. Click "Commit changes"
```

### Step 3: Create `.github/workflows/scrape.yml`
```
1. Go to GitHub repo
2. Click "Add file" → "Create new file"
3. Type filename: ".github/workflows/scrape.yml"
4. Copy entire content from "scrape.yml"
5. Paste it
6. Click "Commit new file"
```

### Step 4: Create/Update `parks_data.json`
```
1. Go to GitHub repo
2. If parks_data.json exists:
   - Click it → edit pencil → delete all → paste from "parks_data_realtime.json" → commit
3. If doesn't exist:
   - Click "Add file" → "Create new file"
   - Type: "parks_data.json"
   - Paste content from "parks_data_realtime.json"
   - Commit
```

---

## ✅ Verify It Works

After uploading:

1. Go to **Actions** tab in GitHub
2. Click **"Update Fall Colors Data"** workflow
3. Click **"Run workflow"** button
4. Wait 30 seconds
5. ✅ If successful: `parks_data.json` will have new timestamp

---

## 🔄 What Happens Next

**Every hour automatically:**
- Scraper runs (GitHub Actions)
- Fetches live data from Ontario Parks
- Updates `parks_data.json`
- Vercel auto-deploys
- Your map shows latest data

**Your followers see live data** when they visit your Vercel URL

---

## 📊 File Summary

| File | Size | Purpose |
|------|------|---------|
| `index_realtime.html` | 11K | Map UI (rename to `index.html`) |
| `scraper.py` | 9.9K | Data scraper (extract live data) |
| `scrape.yml` | 1.1K | GitHub Actions workflow |
| `parks_data_realtime.json` | 11K | Park data (rename to `parks_data.json`) |

---

## 🎯 Result

After uploading → Refresh your Vercel URL

You should see:
✅ Live map with 80+ parks
✅ All parks with current color change %
✅ Sidebar sorted by peak viewing
✅ Auto-updates every hour
✅ Ready to share on Instagram

---

## 📱 Share to Instagram

Copy your Vercel URL (e.g., `https://fall-colors-data.vercel.app`)

Add to bio → Share in stories → Post reels

**Your followers can now see REAL-TIME fall colors!** 🍂
