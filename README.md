# 🚂 Careerly Subscription Service - Railway Deployment

A Flask-based email notification service for the Careerly job portal, optimized for Railway deployment.

## ✨ Features

- ✅ **Email subscription management** (subscribe/unsubscribe)
- ✅ **Professional HTML email notifications** 
- ✅ **CORS support** for frontend integration
- ✅ **Gmail SMTP integration**
- ✅ **Environment variables** for secure configuration
- ✅ **Health check endpoints** for monitoring
- ✅ **Railway deployment ready**

## 🚀 Deploy to Railway

### **Step 1: Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/careerly-subscription-service.git
git push -u origin main
```

### **Step 2: Deploy on Railway**
1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Railway will auto-deploy!

### **Step 3: Set Environment Variables**
In Railway dashboard, go to **Variables** tab and add:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
FLASK_ENV=production
```

### **Step 4: Get Your Deployment URL**
Railway will provide a URL like: `https://your-service-name.railway.app`

## 🔧 Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `config.json`:**
   ```json
   {
     "email": {
       "host": "smtp.gmail.com",
       "port": 587,
       "user": "your-email@gmail.com",
       "password": "your-app-password"
     }
   }
   ```

3. **Run locally:**
   ```bash
   python subscription_api.py
   ```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Service info |
| `GET` | `/health` | Health check |
| `POST` | `/api/subscribe` | Subscribe to job alerts |
| `POST` | `/api/unsubscribe` | Unsubscribe from alerts |
| `POST` | `/api/notify` | Send notifications (internal) |

## 🔒 Gmail Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password:**
   - Go to Google Account settings
   - Security → App passwords
   - Generate password for "Mail"
3. **Use the app password** (not your regular password)

## 🔗 Integration with Django

Update your Django `jobs/signals.py`:

```python
# Replace localhost:5001 with your Railway URL
response = requests.post(
    "https://your-service-name.railway.app/api/notify",
    json={"jobLink": job_link},
    timeout=5
)
```

## 📊 Monitoring

- **Health Check**: `GET /health`
- **Service Info**: `GET /`
- **Railway Logs**: Available in Railway dashboard

## 🛠️ Troubleshooting

### **Emails not sending?**
- Check environment variables are set correctly
- Verify Gmail app password is valid
- Check Railway logs for SMTP errors

### **CORS issues?**
- Service automatically handles CORS for common origins
- Check your frontend URL in the CORS configuration

### **Service not starting?**
- Verify all environment variables are set
- Check Railway build logs
- Ensure `requirements.txt` has all dependencies 