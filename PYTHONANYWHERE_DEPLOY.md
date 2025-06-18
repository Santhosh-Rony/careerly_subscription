# 🐍 PythonAnywhere Deployment Guide

## 🚀 Quick Deploy Steps

### 1. Create Account
- Go to [pythonanywhere.com](https://www.pythonanywhere.com)
- Sign up for **FREE Beginner account**

### 2. Upload Code
**Option A: Git Clone (Recommended)**
```bash
# In PythonAnywhere Console
git clone https://github.com/Santhosh-Rony/careerly_subscription.git
cd careerly_subscription
```

**Option B: Upload Files**
- Use Files tab to upload all files

### 3. Install Dependencies
```bash
# In PythonAnywhere Console
cd careerly_subscription
pip3.10 install --user flask flask-cors requests
```

### 4. Create Web App
1. Go to **Web** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **"Python 3.10"**

### 5. Configure WSGI
1. Click **"WSGI configuration file"** link
2. Replace content with:
```python
import sys
import os

# Replace 'yourusername' with your actual username
project_home = '/home/yourusername/careerly_subscription'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from subscription_api import app as application
```

### 6. Set Environment Variables
In **Web** tab → **Environment variables** section:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=careerly7@gmail.com
EMAIL_PASSWORD=mubixythhyaoirgp
FLASK_ENV=production
```

### 7. Reload & Test
1. Click **"Reload"** button
2. Visit: `https://yourusername.pythonanywhere.com`

## 🧪 Test Endpoints
- `GET /` - Service info
- `GET /health` - Health check
- `POST /api/subscribe` - Subscribe to alerts

## 🔗 Update Django
Set environment variable in your Django project:
```bash
export SUBSCRIPTION_API_URL=https://yourusername.pythonanywhere.com
```

## ✅ Ready to Deploy!
Your subscription service is now optimized for PythonAnywhere! 