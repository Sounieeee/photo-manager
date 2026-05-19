# Photo Album Management System

A production-ready Django web application for creating, organizing, and sharing photo albums with role-based access control and cloud storage integration.

## Features

✨ **Core Features:**
- 📷 Create and manage photo albums
- 🖼️ Upload high-quality photos to albums
- 👥 Invite collaborators with role-based permissions
- 🌍 Share albums publicly or keep them private
- ☁️ Cloud-based image storage with Cloudinary
- 🔒 Secure user authentication and authorization
- 📝 Self-service user registration
- 📱 Responsive design for mobile and desktop

**Access Control:**
- **Owner**: Full control over album (create, edit, delete, manage collaborators)
- **Editor**: Can upload and manage photos within the album
- **Viewer**: Can only view photos in the album

## Tech Stack

- **Backend**: Django 4.2+ with Class-Based Views (CBVs)
- **Database**: PostgreSQL
- **Storage**: Cloudinary for image hosting
- **Frontend**: Bootstrap 5
- **Deployment**: Render
- **Server**: Gunicorn with WhiteNoise for static files

## Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- Cloudinary account (for image storage)
- Render account (for deployment)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd photo_manager_project
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your configuration:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=photo_manager
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
USE_CLOUDINARY=True

SECURE_SSL_REDIRECT=False  # Set to True in production
```

### 5. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` and log in with your superuser credentials.

## Project Structure

```
photo_manager_project/
├── photo_manager/           # Main project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL routing + RegisterView
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
├── albums/                # Photo albums app
│   ├── models.py          # Album, Photo, AlbumCollaborator models
│   ├── views.py           # Class-Based Views with RBAC
│   ├── forms.py           # Album, Photo, and Collaborator forms
│   ├── urls.py            # App URLs (namespace: albums)
│   ├── admin.py           # Django admin configuration
│   └── apps.py            # App configuration
├── templates/             # HTML templates
│   ├── base.html         # Base template with Bootstrap
│   ├── home.html         # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # User registration page
│   └── albums/           # Album-specific templates
│       ├── album_list.html
│       ├── album_detail.html
│       ├── album_form.html
│       ├── album_confirm_delete.html
│       ├── photo_form.html
│       ├── photo_confirm_delete.html
│       ├── collaborators.html
│       ├── add_collaborator.html
│       └── remove_collaborator.html
├── manage.py             # Django management command
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
├── Procfile            # Render deployment configuration
└── render.yaml         # Render infrastructure as code
```

## Models

### Album
- `title` - Album title (unique)
- `description` - Album description
- `owner` - User who created the album (ForeignKey)
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp
- `is_public` - Whether album is publicly visible

**Methods:**
- `can_edit(user)` - Check if user can edit album
- `can_view(user)` - Check if user can view album
- `can_delete(user)` - Check if user can delete album
- `get_photos_count()` - Get number of photos in album

### Photo
- `title` - Photo title (optional)
- `description` - Photo description (optional)
- `image` - Image file (stored in Cloudinary)
- `album` - Album this photo belongs to (ForeignKey)
- `uploaded_by` - User who uploaded the photo
- `uploaded_at` - Upload timestamp
- `updated_at` - Last update timestamp

### AlbumCollaborator
- `album` - Album (ForeignKey)
- `user` - Collaborator user (ForeignKey)
- `role` - Role (owner, editor, viewer)
- `added_at` - When collaborator was added

## Class-Based Views

All views inherit from appropriate Django mixins for authentication and permission checking:

- `AlbumListView` - List all albums accessible to user
- `AlbumDetailView` - View album and its photos
- `AlbumCreateView` - Create new album
- `AlbumUpdateView` - Edit album (editors and owner only)
- `AlbumDeleteView` - Delete album (owner only)
- `PhotoCreateView` - Upload photo to album
- `PhotoUpdateView` - Edit photo details
- `PhotoDeleteView` - Delete photo
- `AlbumCollaboratorsView` - Manage album collaborators
- `AddCollaboratorView` - Add user as collaborator
- `RemoveCollaboratorView` - Remove collaborator

## URL Routes

### Auth
```
/                                 - Home page
/register/                        - User registration
/login/                           - Login
/logout/                          - Logout
```

### Albums
```
/albums/                          - List all accessible albums
/albums/create/                   - Create new album
/albums/<id>/                     - View album details
/albums/<id>/edit/                - Edit album
/albums/<id>/delete/              - Delete album
/albums/<id>/collaborators/       - Manage collaborators
/albums/<id>/collaborators/add/   - Add collaborator
```

### Photos
```
/albums/<id>/photos/create/                  - Upload photo
/albums/<album_id>/photos/<photo_id>/edit/   - Edit photo
/albums/<album_id>/photos/<photo_id>/delete/ - Delete photo
```

## Deployment to Render

### 1. Connect GitHub Repository

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository

### 2. Configure Build and Start Commands

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

**Start Command:**
```bash
gunicorn photo_manager.wsgi:application
```

### 3. Set Environment Variables

In Render dashboard, add the following environment variables:

```
SECRET_KEY=<generate-a-secure-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com

DATABASE_URL=<postgresql-url-from-render>

CLOUDINARY_CLOUD_NAME=<your-cloud-name>
CLOUDINARY_API_KEY=<your-api-key>
CLOUDINARY_API_SECRET=<your-api-secret>
USE_CLOUDINARY=True

SECURE_SSL_REDIRECT=True
```

### 4. Create PostgreSQL Database

1. In Render dashboard, click "New +" and select "PostgreSQL"
2. Create a database instance
3. Copy the DATABASE_URL to your environment variables

### 5. Deploy

Click "Deploy" and wait for the build to complete. Once successful, your app will be live!

### 6. Initialize Superuser

After deployment, create a superuser through the Render shell:

```bash
python manage.py createsuperuser
```

Or access the admin panel and create one through the web interface.

## Usage Examples

### Creating an Album

1. Log in to the application
2. Click "Create Album" in the navigation
3. Fill in the album details (title, description, public/private)
4. Click "Create Album"

### Uploading Photos

1. Go to an album you created
2. Click "Upload Photo"
3. Select image file and add optional title/description
4. Click "Upload Photo"

### Managing Collaborators

1. Go to an album you own
2. Click "Manage Collaborators"
3. Search for a user and select their role
4. Click "Add Collaborator"

### Sharing Albums

- **Public albums**: Enable "Make this album public" when creating/editing
- **Collaborators**: Invite specific users with different permission levels

## Security Features

- 🔐 User authentication required for all operations
- 🛡️ CSRF protection on all forms
- 🔒 Role-based access control (RBAC)
- 🔑 Secure password hashing with Django's default
- 📦 Cloudinary API credentials stored in environment variables
- 🌐 HTTPS enforcement in production
- 🚫 XSS and clickjacking protection

## Performance Optimization

- Database query optimization with `select_related()` and `prefetch_related()`
- Static files compression with WhiteNoise
- Image hosting via Cloudinary CDN
- Database indexes on frequently queried fields
- Pagination for album and collaborator lists

## Troubleshooting

### Database Connection Error

Ensure PostgreSQL is running and `DATABASE_URL` is correctly set:
```bash
# Check connection
python manage.py dbshell
```

### Cloudinary Upload Issues

1. Verify `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET`
2. Check Cloudinary account storage limits
3. Ensure image files are valid

### Static Files Not Loading

```bash
python manage.py collectstatic --clear --noinput
```

### Permission Denied Errors

- Check user roles in admin panel
- Verify album ownership
- Clear browser cache and cookies

## Contributing

1. Create a feature branch
2. Make your changes
3. Push to GitHub
4. Create a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues or questions, please create an issue in the repository or contact the development team.

---

**Built with ❤️ using Django and modern web technologies**
