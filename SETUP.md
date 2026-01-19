# Quick Setup Guide

## Backend Setup (5 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell (if you get execution policy error, see below):
venv\Scripts\activate

# Windows Command Prompt (alternative):
# venv\Scripts\activate.bat

# Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Note: .env file is optional for development
# SQLite database is used by default (no setup needed)
# To use PostgreSQL, create .env file with USE_POSTGRESQL=True

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Backend will run on `http://localhost:8000`

## Frontend Setup (3 minutes)

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Run development server
npm start
```

Frontend will run on `http://localhost:3000`

## First Steps

1. Open `http://localhost:3000`
2. Click "Signup" to create an account
3. Login with your credentials
4. Start using the Library Management System!

## Database Configuration

**SQLite is the default** - no database setup required! The system will automatically create a `db.sqlite3` file in the backend folder.

### To Use PostgreSQL Instead

1. Install PostgreSQL on your system
2. Create a database named `library_db`
3. Create a `.env` file in the `backend` folder with:
   ```
   USE_POSTGRESQL=True
   DB_NAME=library_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

## Troubleshooting

### Windows PowerShell Execution Policy Error

If you get an error like "running scripts is disabled on this system" when activating the virtual environment:

**Option 1: Use Command Prompt instead of PowerShell**
- Open Command Prompt (cmd.exe) instead of PowerShell
- Run: `venv\Scripts\activate.bat`

**Option 2: Use the batch file directly in PowerShell**
```powershell
venv\Scripts\activate.bat
```

**Option 3: Change PowerShell execution policy (requires admin)**
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then you can use: venv\Scripts\activate
```

**Option 4: Bypass for current session only**
```powershell
powershell -ExecutionPolicy Bypass -File venv\Scripts\Activate.ps1
```

### Backend Issues
- **Port 8000 already in use**: Change port with `python manage.py runserver 8001`
- **Database errors**: Make sure migrations are run
- **Module not found**: Activate virtual environment and install requirements

### Frontend Issues
- **Port 3000 already in use**: React will prompt to use another port
- **API connection errors**: Check that backend is running and `REACT_APP_API_URL` is correct
- **npm install fails**: Try deleting `node_modules` and `package-lock.json`, then run `npm install` again
