# Quick Start Guide

Get up and running with Photo Album Manager in minutes!

## Option 1: Using Docker Compose (Recommended for Development)

### Prerequisites
- Docker Desktop installed

### Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd photo_manager_project

# 2. Create .env file (if not exists)
cp .env.example .env

# 3. Update Cloudinary credentials in .env
# Edit .env and add your Cloudinary credentials

# 4. Start the application
docker-compose up -d

# 5. Run migrations
docker-compose exec web python manage.py migrate

# 6. Create superuser
docker-compose exec web python manage.py createsuperuser

# 7. Access the app
# App: http://localhost:8000
# Admin: http://localhost:8000/admin/

# To stop:
docker-compose down
```

## Option 2: Manual Setup (PostgreSQL Required)

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- pip and virtualenv

### Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd photo_manager_project

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env

# 5. Update .env with your settings:
#    - CLOUDINARY credentials
#    - Database connection details
nano .env  # or use your favorite editor

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Collect static files
python manage.py collectstatic

# 9. Run development server
python manage.py runserver

# 10. Access the app
# App: http://localhost:8000
# Admin: http://localhost:8000/admin/
```

## Configuration

### Cloudinary Setup

1. Sign up at https://cloudinary.com/
2. Get your credentials from Dashboard:
   - Cloud Name
   - API Key
   - API Secret
3. Update `.env` file:
   ```
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

### Database Setup

For development, the `.env` file comes pre-configured for:
- PostgreSQL on localhost
- Database: `photo_manager`
- User: `postgres`
- Password: `postgres`

Create the database:
```bash
createdb -U postgres photo_manager
```

## First Steps

1. **Log in to admin panel**
   - URL: http://localhost:8000/admin/
   - Use superuser credentials

2. **Create your first album**
   - Go to http://localhost:8000/albums/
   - Click "Create Album"
   - Upload photos

3. **Invite collaborators**
   - Go to album details
   - Click "Manage Collaborators"
   - Add users with different roles

4. **Make albums public**
   - Edit album settings
   - Enable "Make this album public"
   - Share with anyone

## Useful Commands

```bash
# Run development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Create test data
python manage.py shell
# Then in the shell:
# from django.contrib.auth.models import User
# from albums.models import Album
# user = User.objects.create_user('testuser', 'test@example.com', 'password')
# Album.objects.create(title='Test Album', owner=user)

# Run tests
python manage.py test

# Check for issues
python manage.py check

# Access database shell
python manage.py dbshell

# Interactive Django shell
python manage.py shell
```

## Troubleshooting

### Issue: "Cannot connect to database"
```bash
# Check PostgreSQL is running
# On Linux/Mac
brew services list
# On Windows, check Services

# Update .env with correct credentials
DB_HOST=localhost
DB_PORT=5432
```

### Issue: "ModuleNotFoundError"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "Static files not found"
```bash
# Recollect static files
python manage.py collectstatic --clear --noinput
```

### Issue: "Image upload fails"
1. Check Cloudinary credentials in .env
2. Verify image file format (JPG, PNG, GIF, WebP)
3. Check image file size
4. Check Cloudinary account limits

## Next Steps

1. **Customize the theme** - Edit CSS in `templates/base.html`
2. **Add more features** - Check `README.md` for architecture
3. **Deploy to Render** - Follow `DEPLOYMENT.md` guide
4. **Run tests** - Create tests in `albums/tests.py`

## Getting Help

- Check the README.md for detailed documentation
- Review DEPLOYMENT.md for production setup
- Check Django documentation: https://docs.djangoproject.com/
- Ask in GitHub issues

---

**Happy coding! 🚀**
