# Library Management System

A full-stack Library Management System built with Django REST Framework (backend) and React (frontend).

## Features

- **User Authentication**: JWT-based authentication with login/signup
- **Book Management**: Add, edit, list, and search books
- **Member Management**: Register and manage library members
- **Issue/Return Books**: Issue books to members and track returns
- **Dashboard**: Overview of library statistics and recent activities
- **Responsive UI**: Modern and user-friendly interface

## Tech Stack

### Backend
- Django 4.2.7
- Django REST Framework
- JWT Authentication (djangorestframework-simplejwt)
- PostgreSQL (or SQLite for development)
- CORS headers for cross-origin requests

### Frontend
- React 18.2.0
- React Router DOM
- Axios for API calls
- Context API for state management

## Project Structure

```
library-project/
├── backend/
│   ├── library_project/     # Django project settings
│   ├── library/             # Main app
│   │   ├── models.py        # Book, Member, IssueRecord models
│   │   ├── views.py         # API viewsets
│   │   ├── serializers.py   # DRF serializers
│   │   └── urls.py          # URL routing
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── contexts/        # React contexts
│   │   ├── services/        # API service
│   │   └── App.js
│   ├── public/
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL (optional, SQLite can be used for development)
- pip and npm

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

4. **Run development server:**
   ```bash
   npm start
   ```

   Frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/token/` - Login (get JWT tokens)
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/auth/register/` - Register new user
- `GET /api/auth/me/` - Get current user info

### Books
- `GET /api/books/` - List all books (with search)
- `GET /api/books/{id}/` - Get book details
- `POST /api/books/` - Create new book
- `PUT /api/books/{id}/` - Update book
- `DELETE /api/books/{id}/` - Delete book
- `GET /api/books/available/` - Get available books

### Members
- `GET /api/members/` - List all members
- `GET /api/members/{id}/` - Get member details
- `GET /api/members/{id}/issues/` - Get member's issue records

### Issue Records
- `GET /api/issues/` - List all issue records
- `POST /api/issues/issue/` - Issue a book
- `POST /api/issues/return_book/` - Return a book

## Database Models

### Book
- title, author, isbn, publication_date
- total_copies, available_copies
- description

### Member
- user (OneToOne with Django User)
- member_id, phone, address
- date_joined, is_active

### IssueRecord
- book, member
- issue_date, due_date, return_date
- status (issued/returned/overdue)
- fine_amount

## Deployment

### Backend Deployment (Heroku/Railway/PythonAnywhere)

See `DEPLOYMENT.md` for detailed deployment instructions.

### Frontend Deployment (Netlify/Vercel)

1. Build the React app:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy the `build` folder to your hosting service.

3. Set environment variable:
   - `REACT_APP_API_URL`: Your deployed backend API URL

## Development Notes

- Use SQLite for local development (change in `settings.py`)
- CORS is configured to allow all origins in DEBUG mode
- JWT tokens are stored in localStorage
- Access token expires in 1 hour, refresh token in 7 days

## License

MIT License
