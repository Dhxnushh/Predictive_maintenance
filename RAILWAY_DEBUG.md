# 🚂 Railway Deployment Quick Guide

## ✅ Fixed: PORT Variable Issue

**Problem:** `'$PORT' is not a valid integer`  
**Solution:** Using startup script that properly handles environment variables

## 🔧 Start Commands (All Fixed)

The app now uses `start.sh` which properly handles the PORT variable:

**Option 1: Shell Script (Default)**
```bash
./start.sh
```

**Option 2: Python Entrypoint (Fallback)**
```bash
python entrypoint.py
```

Both methods correctly read the `$PORT` environment variable.

---

## Current Issue: 502 Bad Gateway

The app built successfully but isn't responding. Here's how to fix it:

## 🔍 Step 1: Check Logs

**In Railway Dashboard:**
1. Go to your service
2. Click "Deployments" tab
3. Click on the latest deployment
4. View the **Deploy Logs**

Look for errors after "Starting deployment..."

## 🔧 Step 2: Common Fixes

### Fix 1: Switch to Dockerfile (Recommended)

Railway's nixpacks can be finicky. Use Docker instead:

1. **In Railway:** Settings → Builder
2. **Select:** "Dockerfile"
3. **Click:** Redeploy

The Dockerfile is already configured and tested.

### Fix 2: Check Model Files

Ensure the models directory is committed:

```bash
git add models/
git commit -m "Add model files"
git push
```

### Fix 3: Environment Variables

In Railway Dashboard → Variables, ensure:
- `PORT` is NOT manually set (Railway auto-sets this)
- `ENV` = `production` (optional)

## 🧪 Step 3: Test Locally

Run with Railway's environment:

```bash
# Windows
$env:PORT=8000
python app.py

# Linux/Mac
export PORT=8000
python app.py
```

Visit: http://localhost:8000/health

Should return:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "model_loaded": true
}
```

## 📝 Step 4: View Detailed Logs

If you have Railway CLI:

```bash
railway logs
```

Or in dashboard: Deployments → Latest → View Logs

## ✅ Expected Startup Logs

When working correctly, you should see:

```
🚀 Starting Predictive Maintenance API...
📍 Environment: production
🔌 Port: 8000
✓ Model loaded successfully
✓ Monitoring service initialized
✓ Predictive Maintenance API started successfully
INFO: Uvicorn running on http://0.0.0.0:8000
```

## 🆘 Still Not Working?

**Check for these specific errors:**

1. **"Model not found"** → Models directory not deployed
2. **"Port binding failed"** → PORT environment issue
3. **"Import error"** → Missing dependency in requirements.txt
4. **"Permission denied"** → File permissions issue

## 💡 Quick Test URLs

Once deployed, test these endpoints:

- Health: `https://your-app.railway.app/health`
- Root: `https://your-app.railway.app/`
- Dashboard: `https://your-app.railway.app/dashboard`
- Docs: `https://your-app.railway.app/docs`

## 🎯 Next Steps

1. **Switch to Dockerfile builder** (most reliable)
2. **Check deploy logs** for specific errors
3. **Verify model files** are in repository
4. **Test health endpoint** first

---

**Need the logs?** Share them and I can help debug further!
