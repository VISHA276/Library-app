# Render Deployment Guide

This guide will help you deploy the Library Management System to Render.

## Prerequisites

1. **GitHub Account** - Push your code to GitHub
2. **Render Account** - Sign up at [https://render.com](https://render.com)

## Steps to Deploy

### 1. Push Code to GitHub

```bash
cd c:\Users\EC1048\Desktop\library-project

# If not already initialized
git init
git add .
git commit -m "Initial commit for Render deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/library-project.git
git push -u origin main
```

### 2. Create a Render Account

- Visit [https://render.com](https://render.com)
- Sign up with GitHub
- Connect your GitHub account

### 3. Deploy Backend Service

1. Go to Render Dashboard
2. Click **"Create +"** → **"Web Service"**
3. Select your `library-project` repository
4. Configure:
   - **Name**: `library-backend`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command**: `gunicorn library_project.wsgi`
   - **Plan**: Free tier

5. **Add Environment Variables**:
   - `DEBUG`: `False`
   - `PYTHONUNBUFFERED`: `1`
   - `SECRET_KEY`: (generate a strong secret key)
   - `ALLOWED_HOSTS`: `library-backend.onrender.com`
   - `CORS_ALLOWED_ORIGINS`: `https://library-frontend.onrender.com`

6. Click **Create Web Service**

### 4. Deploy Frontend Service

1. Click **"Create +"** → **"Static Site"** (or **"Web Service"** for Node)
2. Select your `library-project` repository
3. Configure:
   - **Name**: `library-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
   - **Plan**: Free tier

4. **Add Environment Variables**:
   - `REACT_APP_API_URL`: `https://library-backend.onrender.com`

5. Click **Create**

### 5. Create Database (PostgreSQL)

1. On Render Dashboard, click **"Create +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `library-db`
   - **Database**: `library`
   - **User**: `library_user`
   - **Region**: Your preferred region
   - **Plan**: Free tier

3. Copy the **Internal Database URL**

### 6. Link Database to Backend

1. Go to your Backend Service settings
2. Add Environment Variables:
   - `USE_POSTGRESQL`: `True`
   - `DATABASE_URL`: (paste the PostgreSQL internal URL)

3. Or use individual variables:
   - `DB_HOST`: (from PostgreSQL service)
   - `DB_NAME`: `library`
   - `DB_USER`: `library_user`
   - `DB_PASSWORD`: (from PostgreSQL service)
   - `DB_PORT`: `5432`

### 7. Generate Secret Key

For security, generate a strong SECRET_KEY:

```bash
# In Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or visit: https://djecrety.ir/

### 8. Verify Deployment

- Backend URL: `https://library-backend.onrender.com`
- Frontend URL: `https://library-frontend.onrender.com`
- Admin Panel: `https://library-backend.onrender.com/admin`

### 9. Create Superuser (Optional)

```bash
# Via Render Shell or Console
python manage.py createsuperuser
```

## Troubleshooting

### Static Files Not Loading
- Ensure `STATIC_ROOT` is set in settings.py
- Run: `python manage.py collectstatic --noinput`

### CORS Errors
- Update `CORS_ALLOWED_ORIGINS` to match your frontend URL
- Set `CORS_ALLOW_CREDENTIALS = True`

### Database Connection Issues
- Verify DATABASE_URL format
- Check that PostgreSQL service is active
- Run migrations: `python manage.py migrate`

### 404 on Frontend Routes
- Ensure `_redirects` or `vercel.json` is configured
- Check build directory setting

## Monitoring

- View logs: Render Dashboard → Service → Logs
- Monitor metrics: Service → Metrics
- Setup alerts: Service → Alerts

## Helpful Resources

- [Render Django Deployment](https://render.com/docs/deploy-django)
- [Render PostgreSQL](https://render.com/docs/databases)
- [Django Security Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
