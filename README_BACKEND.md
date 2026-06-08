# Ashanti Community Reports Backend - FastAPI

A minimal FastAPI backend for the Ashanti Community Reports Platform. This is a demo/MVP backend with SQLite database and JWT authentication.

## Quick Start

### 1. Install Dependencies

```bash
cd ashanti-backend
pip install -r requirements.txt
```

### 2. Seed Database with Test Data

```bash
python seed_data.py
```

You should see:
```
🌱 Seeding database with test data...
✅ Created regions
✅ Created MMDAs
✅ Created problem categories
✅ Created test users
   - Citizen: citizen@example.com / password123
   - Minister: minister@example.com / password123
   - Official: official@example.com / password123
✅ Created sample reports
🌱 Database seeding completed successfully!
```

### 3. Start the Backend Server

```bash
python main.py
```

Server runs on: **http://localhost:5000**

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:5000
```

### 4. Test the API

#### Health Check
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "ok", "message": "Ashanti Community Reports API is running"}
```

#### API Documentation
Open in browser: **http://localhost:5000/docs**

This shows the interactive API documentation where you can test all endpoints.

---

## Test Credentials

Use these to test login in the frontend:

| Role | Email | Password |
|------|-------|----------|
| Citizen | citizen@example.com | password123 |
| Minister | minister@example.com | password123 |
| Official | official@example.com | password123 |

---

## API Endpoints

### Authentication
- `POST /auth/login` - Login user
- `POST /auth/signup` - Create new account
- `GET /users/me` - Get current user
- `PATCH /users/update` - Update user
- `DELETE /users/{user_id}` - Delete user

### App Data
- `GET /app/regions` - Get all regions
- `GET /app/mmdas/{region_id}` - Get MMDAs for region
- `GET /app/problem-categories` - Get problem categories

### Reports
- `POST /reports/submit` - Submit new report
- `GET /reports/my-reports` - Get user's reports
- `GET /reports/minister-dashboard` - Get all reports
- `GET /reports/{report_id}` - Get specific report
- `PATCH /reports/{report_id}` - Update report
- `DELETE /reports/{report_id}` - Delete report

---

## Database Schema

### Users
- `id` (UUID primary key)
- `email` (unique)
- `display_name`
- `phone`
- `hashed_password`
- `role` (citizen, minister, glinax)
- `region`
- `is_active`
- `created_at`

### Reports
- `id` (UUID primary key)
- `user_id` (foreign key)
- `region`
- `mmda`
- `community`
- `category`
- `title`
- `description`
- `severity` (low, medium, high)
- `ghana_postgps` (location)
- `file_url` (optional)
- `status` (pending, in_progress, resolved)
- `created_at`
- `updated_at`

### Regions
- `id` (primary key)
- `name` (unique)

### MMDAs
- `id` (primary key)
- `name`
- `region_id` (foreign key)

### Problem Categories
- `id` (primary key)
- `name` (unique)

---

## Environment Variables

Edit `.env` to configure:

```env
DATABASE_URL=sqlite:///./ashanti.db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

For production, use a real database URL like:
```
DATABASE_URL=postgresql://user:password@localhost/ashanti
```

---

## File Structure

```
ashanti-backend/
├── main.py                 # FastAPI app + all route handlers
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic validation schemas
├── database.py            # Database configuration
├── auth.py                # JWT & password utilities
├── seed_data.py           # Script to populate test data
├── requirements.txt       # Python dependencies
├── .env                   # Configuration
├── .gitignore            # Git ignore rules
└── README_BACKEND.md     # This file
```

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:** Use a different port
```bash
uvicorn main:app --host 0.0.0.0 --port 5001
```

### Issue: "Database is locked" (SQLite)
**Solution:** Delete the database file and reseed
```bash
rm ashanti.db
python seed_data.py
```

### Issue: Frontend can't connect to backend
**Solution:** Ensure backend is running on http://localhost:5000 and check:
1. Frontend `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:5000`
2. No firewall blocking port 5000
3. CORS is enabled (it is by default)

---

## Troubleshooting

### Check if backend is running
```bash
curl http://localhost:5000/health
```

### View API docs
Open browser: **http://localhost:5000/docs**

### Enable debug logging
Edit `main.py` and uncomment:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Reset database and reseed
```bash
rm ashanti.db
python seed_data.py
```

---

## Next Steps for Production

1. **Use a real database** - Replace SQLite with PostgreSQL
2. **Environment variables** - Use proper secret management
3. **Authentication** - Implement proper JWT token validation
4. **Validation** - Add more rigorous input validation
5. **Rate limiting** - Prevent API abuse
6. **Logging** - Add structured logging
7. **Error handling** - Better error messages
8. **Testing** - Write unit and integration tests
9. **Documentation** - Add API documentation
10. **Deployment** - Deploy to AWS, Azure, or Heroku

---

## Support

If you encounter issues:
1. Check the console output for error messages
2. Visit http://localhost:5000/docs to test endpoints
3. Check database exists: `ls ashanti.db`
4. Reseed if needed: `python seed_data.py`

---

**Built with FastAPI for the Ashanti Community Reports Platform** 🚀
