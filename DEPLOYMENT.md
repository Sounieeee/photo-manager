# Deployment Guide - Photo Album Manager

This guide provides step-by-step instructions for deploying the Photo Album Manager to Render.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Prepare Repository](#prepare-repository)
3. [Set Up Cloudinary](#set-up-cloudinary)
4. [Deploy to Render](#deploy-to-render)
5. [Post-Deployment Steps](#post-deployment-steps)
6. [Monitoring & Troubleshooting](#monitoring--troubleshooting)

## Prerequisites

Before deploying, ensure you have:

- ✅ GitHub account with the repository pushed
- ✅ Render account (https://render.com/)
- ✅ Cloudinary account (https://cloudinary.com/)
- ✅ All code committed and pushed to GitHub

## Prepare Repository

### 1. Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: Photo Album Manager"
git remote add origin https://github.com/yourusername/photo-manager.git
git branch -M main
git push -u origin main
```

### 2. Update .env.example

Ensure `.env.example` is in the repository with all required variables (but no secret values):

```bash
git add .env.example
git commit -m "Add environment template"
git push
```

### 3. Ensure .env is in .gitignore

Make sure `.env` is NOT committed to GitHub:

```bash
# Check if .env is in .gitignore
cat .gitignore | grep ".env"

# If not, add it
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Ensure .env is gitignored"
git push
```

## Set Up Cloudinary

### 1. Create Cloudinary Account

1. Go to https://cloudinary.com/
2. Sign up for a free account
3. Verify your email

### 2. Get API Credentials

1. Go to your Cloudinary Dashboard
2. In the "Account Details" section, you'll find:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

Save these values securely - you'll need them for Render.

## Deploy to Render

### Step 1: Connect GitHub Repository

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** button
3. Select **Web Service**
4. Click **Connect** next to your GitHub repository
5. Authorize Render with your GitHub account
6. Select the `photo_manager_project` repository

### Step 2: Configure Web Service

Fill in the following details:

| Field | Value |
|-------|-------|
| **Name** | `photo-album-manager` |
| **Environment** | `Python 3` |
| **Region** | `Oregon` (or your preferred region) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn photo_manager.wsgi:application` |

### Step 3: Set Environment Variables

Click on **Environment** in the left sidebar and add the following variables:

**Required Variables:**

```
SECRET_KEY=<generate-a-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com

CLOUDINARY_CLOUD_NAME=<your-cloudinary-cloud-name>
CLOUDINARY_API_KEY=<your-cloudinary-api-key>
CLOUDINARY_API_SECRET=<your-cloudinary-api-secret>

SECURE_SSL_REDIRECT=True
USE_CLOUDINARY=True
```

**To generate a strong SECRET_KEY:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or use an online generator: https://djecrety.ir/

### Step 4: Create PostgreSQL Database

1. In Render Dashboard, click **New +**
2. Select **PostgreSQL**
3. Fill in details:
   - **Name**: `photo-album-db`
   - **Database**: `photo_manager`
   - **User**: `postgres`
   - **Region**: Same as web service
   - **Plan**: `Free`

4. Click **Create Database**

5. Once created, copy the **Database URL**

### Step 5: Add Database URL to Web Service

1. Go back to your Web Service settings
2. Click **Environment**
3. Add the PostgreSQL URL with different variable names:

```
DB_HOST=<from-database-url>
DB_NAME=photo_manager
DB_USER=postgres
DB_PASSWORD=<from-database-url>
DB_PORT=5432
```

Or better yet, use:
```
DATABASE_URL=<full-postgresql-url>
```

### Step 6: Deploy

1. Click **Deploy** button
2. Watch the build logs for any errors
3. Once deployment completes, visit your live URL

### Step 7: Initialize Database

Once deployment succeeds:

1. Go to your Render service dashboard
2. Click the **Shell** tab
3. Run these commands:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

For the superuser:
- **Username**: admin
- **Email**: your-email@example.com
- **Password**: (choose a strong password)

## Post-Deployment Steps

### 1. Test the Application

1. Visit your live URL: `https://your-app-name.onrender.com`
2. Try logging in with your superuser credentials
3. Create a test album and upload a photo

### 2. Access Admin Panel

1. Go to `https://your-app-name.onrender.com/admin/`
2. Log in with your superuser credentials
3. Verify that albums and photos are stored correctly

### 3. Test Cloudinary Integration

1. Upload a test photo through the application
2. Verify the image displays correctly
3. Check Cloudinary dashboard to see the uploaded image

### 4. Enable Email (Optional)

For production, configure email settings:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

## Monitoring & Troubleshooting

### View Logs

1. In Render dashboard, go to your Web Service
2. Click **Logs** tab
3. Monitor for errors

### Common Issues

#### Issue: Build Failure - "ModuleNotFoundError"

**Solution:**
```bash
# Ensure all dependencies are in requirements.txt
pip freeze > requirements.txt
git push
# Redeploy from Render dashboard
```

#### Issue: Database Connection Error

**Solution:**
1. Verify DATABASE_URL is correct
2. Check database is running: Render → PostgreSQL → Status
3. Run migrations again through Shell

#### Issue: Static Files Not Loading

**Solution:**
```bash
# Through Render Shell:
python manage.py collectstatic --clear --noinput
```

#### Issue: Images Not Uploading

**Solution:**
1. Verify Cloudinary credentials in Render environment
2. Check Cloudinary account limits
3. Ensure image file size is reasonable
4. Check browser console for CORS errors

#### Issue: 502 Bad Gateway Error

**Solution:**
1. Check the logs for errors
2. Restart the service from Render dashboard
3. Verify gunicorn is starting correctly
4. Check if database migrations ran successfully

### Monitor Performance

1. **Response Times**: Check Render metrics
2. **Error Rates**: Monitor logs daily
3. **Storage Usage**: Check Cloudinary dashboard
4. **Database Size**: Monitor PostgreSQL in Render

### Keep Running During Grading

Render free tier services can spin down after 15 minutes of inactivity. To keep your service running:

1. Go to Web Service settings
2. Ensure it's not on a free tier that spins down
3. Or upgrade to Starter plan ($7/month)
4. Keep accessing the app regularly during grading period

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-xxxxx` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed domains | `your-app.onrender.com` |
| `DB_NAME` | Database name | `photo_manager` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `xxxxx` |
| `DB_HOST` | Database host | `dpg-xxxxx.postgres.render.com` |
| `DB_PORT` | Database port | `5432` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | `xxxxx` |
| `CLOUDINARY_API_KEY` | Cloudinary API key | `xxxxx` |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | `xxxxx` |
| `SECURE_SSL_REDIRECT` | Force HTTPS | `True` |
| `USE_CLOUDINARY` | Use Cloudinary for storage | `True` |

## Deployment Checklist

- [ ] GitHub repository created and code pushed
- [ ] Cloudinary account created and credentials obtained
- [ ] Render account created
- [ ] Web Service created on Render
- [ ] PostgreSQL database created on Render
- [ ] All environment variables set
- [ ] Build and start commands configured
- [ ] Initial deployment successful
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Application tested in browser
- [ ] Admin panel accessible
- [ ] Photo upload tested
- [ ] Images display correctly from Cloudinary

## Support & Resources

- **Render Documentation**: https://docs.render.com/
- **Django Documentation**: https://docs.djangoproject.com/
- **Cloudinary Documentation**: https://cloudinary.com/documentation
- **PostgreSQL**: https://www.postgresql.org/docs/

---

**🎉 Your Photo Album Manager is now live on Render!**
