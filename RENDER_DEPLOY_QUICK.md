# Deploy to Render - Step by Step Guide

Your code is now pushed to GitHub and ready for deployment to Render!

## Quick Start (5 minutes)

### Step 1: Create Render Account
1. Go to https://render.com
2. Click **Sign Up** (or **Sign In**)
3. Select **Sign up with GitHub**
4. Authorize Render to access your GitHub account

### Step 2: Deploy Backend API

1. On Render Dashboard, click **+ New**
2. Select **Web Service**
3. Click **Connect a repository**
4. Search for and select `Library-app` repository
5. Click **Connect**

**Configure Backend Service:**
- **Name:** `library-backend`
- **Environment:** `Python 3`
- **Region:** Choose closest to you
- **Branch:** `main`
- **Build Command:** 
  ```
  pip install -r requirements.txt && python manage.py migrate
  ```
- **Start Command:**
  ```
  gunicorn library_project.wsgi
  ```
- **Plan:** Free

**Add Environment Variables** (Click **Add Secret File** or **Environment**)
- `DEBUG` = `False`
- `SECRET_KEY` = (generate from https://djecrety.ir/)
- `PYTHONUNBUFFERED` = `1`
- `ALLOWED_HOSTS` = `library-backend.onrender.com`

6. Click **Create Web Service**

💡 **Note:** Render will auto-deploy from GitHub. Wait for build to complete (~3-5 min).

### Step 3: Deploy Frontend React App

1. On Render Dashboard, click **+ New**
2. Select **Static Site** (or **Web Service** for more control)
3. Click **Connect a repository**
4. Search for and select `Library-app` repository
5. Click **Connect**

**Configure Frontend Service:**
- **Name:** `library-frontend`
- **Environment:** Leave default (or `Node`)
- **Region:** Same as backend
- **Branch:** `main`
- **Build Command:**
  ```
  npm install && npm run build
  ```
- **Publish Directory:** `build` (if web service) or `frontend/build` (if static)
- **Root Directory:** `frontend`
- **Plan:** Free

**Add Environment Variables:**
- `REACT_APP_API_URL` = `https://library-backend.onrender.com`
- `NODE_VERSION` = `20`

6. Click **Create Static Site** or **Create Web Service**

### Step 4: Create Database (Optional)

If you want persistent data:

1. Click **+ New**
2. Select **PostgreSQL**
3. Configure:
   - **Name:** `library-db`
   - **Database:** `library`
   - **User:** `library_user`
   - **Region:** Same as backend
   - **Plan:** Free

4. Copy the **Internal Database URL**

### Step 5: Connect Database to Backend

1. Go to **library-backend** service
2. Click **Environment** 
3. Add new variable:
   - **Key:** `DATABASE_URL`
   - **Value:** (Paste the PostgreSQL URL from Step 4)

4. Click **Save Changes**
5. Backend will auto-redeploy

### Step 6: Connect Frontend to Backend

1. Go to **library-frontend** service
2. Click **Environment**
3. Update/Add:
   - **Key:** `REACT_APP_API_URL`
   - **Value:** `https://library-backend.onrender.com`

4. Click **Save Changes**
5. Frontend will auto-redeploy

## Verify Deployment

✅ **Backend API:** 
- URL: `https://library-backend.onrender.com`
- Test API: `https://library-backend.onrender.com/api/books/`
- Admin: `https://library-backend.onrender.com/admin`

✅ **Frontend App:**
- URL: `https://library-frontend.onrender.com`

## Update CORS Settings (If Needed)

If you get CORS errors:

1. Go to Backend Service
2. Click **Environment**
3. Update `CORS_ALLOWED_ORIGINS`:
   ```
   https://library-frontend.onrender.com
   ```

## Troubleshooting

### Backend build fails
- Check build logs in Render dashboard
- Ensure `backend/requirements.txt` is valid
- Run locally: `pip install -r requirements.txt`

### Frontend shows "Cannot reach API"
- Verify `REACT_APP_API_URL` is correct
- Check Backend service is running
- Check CORS configuration

### Database not connecting
- Verify `DATABASE_URL` format
- Check PostgreSQL service status
- Run migrations: add to Build Command

### Redeploy after changes
- Push to GitHub `main` branch
- Render auto-deploys (takes 2-5 min)
- Or manually redeploy from Render dashboard

## Your Live Application URLs

Once deployed:
- **Backend API:** https://library-backend.onrender.com
- **Frontend App:** https://library-frontend.onrender.com
- **Admin Dashboard:** https://library-backend.onrender.com/admin

## Next Steps

1. ✅ Create superuser (via Render shell):
   ```bash
   python manage.py createsuperuser
   ```

2. ✅ Load sample data (if available):
   ```bash
   python manage.py load_sample_data
   ```

3. ✅ Test the application with real users

4. ✅ Monitor logs and performance in Render dashboard

---

**Questions?** Check the full RENDER_DEPLOYMENT.md guide in your project.
