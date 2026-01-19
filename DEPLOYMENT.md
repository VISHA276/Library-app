# Deployment Guide

This guide covers deploying the Library Management System to various platforms.

## Backend Deployment

### Option 1: Heroku

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   cd backend
   heroku create your-library-app
   ```

3. **Add PostgreSQL addon:**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-library-app.herokuapp.com
   heroku config:set CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

5. **Update requirements.txt** to include gunicorn:
   ```
   gunicorn==21.2.0
   ```

6. **Deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku git:remote -a your-library-app
   git push heroku main
   ```

7. **Run migrations:**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Option 2: Railway

1. **Create Railway account** and new project

2. **Connect GitHub repository** or deploy directly

3. **Add PostgreSQL service** in Railway dashboard

4. **Set environment variables** in Railway:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app.railway.app`
   - `CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com`
   - Database variables (auto-set by Railway PostgreSQL)

5. **Set build command:**
   ```
   pip install -r requirements.txt
   ```

6. **Set start command:**
   ```
   python manage.py migrate && gunicorn library_project.wsgi
   ```

7. **Deploy** - Railway will auto-deploy on git push

### Option 3: PythonAnywhere

1. **Create account** on PythonAnywhere

2. **Upload project files** via Files tab or Git

3. **Create virtual environment:**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 library-env
   pip install -r requirements.txt
   ```

4. **Set up database:**
   - Use MySQL or PostgreSQL (Web tab > Databases)
   - Update `settings.py` with database credentials

5. **Configure WSGI file:**
   - Go to Web tab > WSGI configuration file
   - Point to your Django project

6. **Set environment variables** in WSGI file or bash console

7. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

8. **Reload web app** from Web tab

## Frontend Deployment

### Option 1: Netlify

1. **Build the React app:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy via Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   netlify login
   netlify deploy --prod --dir=build
   ```

3. **Or connect GitHub repository:**
   - Go to Netlify dashboard
   - New site from Git
   - Select repository
   - Build settings:
     - Build command: `npm run build`
     - Publish directory: `build`

4. **Set environment variables:**
   - Site settings > Environment variables
   - Add `REACT_APP_API_URL` with your backend URL

5. **Add `_redirects` file** in `public/` folder:
   ```
   /*    /index.html   200
   ```

### Option 2: Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd frontend
   vercel
   ```

3. **Or connect GitHub:**
   - Go to Vercel dashboard
   - Import project
   - Set build command: `npm run build`
   - Set output directory: `build`

4. **Set environment variables:**
   - Project settings > Environment Variables
   - Add `REACT_APP_API_URL`

5. **Add `vercel.json`** in frontend root:
   ```json
   {
     "rewrites": [
       { "source": "/(.*)", "destination": "/index.html" }
     ]
   }
   ```

### Option 3: GitHub Pages

1. **Install gh-pages:**
   ```bash
   cd frontend
   npm install --save-dev gh-pages
   ```

2. **Update package.json:**
   ```json
   {
     "homepage": "https://yourusername.github.io/library-project",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d build"
     }
   }
   ```

3. **Deploy:**
   ```bash
   npm run deploy
   ```

4. **Set environment variable** in GitHub Actions or build script

## Production Configuration

### Backend Settings

Update `backend/library_project/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-backend-domain.com']
CORS_ALLOWED_ORIGINS = ['https://your-frontend-domain.com']
CORS_ALLOW_ALL_ORIGINS = False  # Important for production
```

### Frontend Settings

Update `frontend/.env.production`:

```
REACT_APP_API_URL=https://your-backend-domain.com/api
```

### Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set specific `CORS_ALLOWED_ORIGINS`
- [ ] Use HTTPS for both frontend and backend
- [ ] Set up database backups
- [ ] Use environment variables for sensitive data
- [ ] Enable Django security middleware
- [ ] Set up logging and monitoring

## Environment Variables Summary

### Backend (.env)
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-backend-domain.com
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Frontend (.env)
```
REACT_APP_API_URL=https://your-backend-domain.com/api
```

## Troubleshooting

### CORS Issues
- Ensure `CORS_ALLOWED_ORIGINS` includes your frontend URL
- Check that `CORS_ALLOW_CREDENTIALS=True` if using cookies
- Verify backend allows OPTIONS requests

### Database Connection
- Check database credentials
- Ensure database server is accessible
- Run migrations after deployment

### Build Errors
- Check Node.js and Python versions
- Verify all dependencies are installed
- Check for missing environment variables

### 404 Errors (Frontend)
- Ensure redirect rules are configured
- Check that React Router is set up correctly
- Verify build output directory
