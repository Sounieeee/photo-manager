# 📷 Django Photo Album Management System

A production-ready, full-stack web application built with **Django** for securely creating, organizing, and sharing photo albums. It integrates **Role-Based Access Control (RBAC)**, **Cloudinary Media Storage**, and a PostgreSQL database, ready to be deployed instantly on **Render**.

---

## 🌟 Overview of the App

This application acts as a personal or collaborative cloud photo manager. It solves the problem of securely organizing images by allowing users to create custom "Albums", upload their pictures, and selectively invite other registered users to collaborate on those albums. 

The system relies entirely on native Django Class-Based Views (CBVs) to handle rapid, secure CRUD operations and utilizes decoupled environment variables for enterprise-grade security.

### Key Features
* **User Accounts:** Fully integrated registration, login, and secure sessions.
* **Album Management:** Create public or private albums with titles and descriptions.
* **Photo Uploads:** Upload image files directly to the cloud.
* **Collaborator System:** Invite other registered users to your private albums.
* **Rich Admin Panel:** A fully customized Django admin panel with real-time stats and metrics for staff users.

---

## 🏗️ Technical Details & Architecture

This project was built following industry-standard patterns and strictly adheres to the following architectural requirements:

### 1. Class-Based Views (CBVs)
All core CRUD routing is handled by Django CBVs (`ListView`, `CreateView`, `UpdateView`, `DeleteView`) located in `albums/views.py`. This ensures code reusability, minimizes boilerplate, and speeds up the handling of forms and object queries.

### 2. Role-Based Access Control (RBAC)
Security is enforced using Custom Mixins (`AlbumOwnerMixin`, `AlbumEditMixin`, `AlbumAccessMixin`).
When a user accesses an album, the system verifies their role:
* **Owner:** Full administrative control. Can delete the album and manage collaborators.
* **Editor:** Can view the album, upload new photos, and edit existing photo metadata.
* **Viewer:** Read-only access. Can view the photos inside the private album but cannot upload.

### 3. Cloud Storage (Cloudinary)
Local media storage is disabled for production. The application seamlessly integrates with the Cloudinary API (via `django-cloudinary-storage`). All photos uploaded by users are streamed directly to a Cloudinary bucket, bypassing local server disks and ensuring persistence across server restarts.

---

## 📖 Tutorial: How to Use the App

### Step 1: Running the Application Locally
If you want to test the application on your own computer before uploading it to the cloud:
1. Clone this repository to your computer.
2. Open a terminal in the project folder and create a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # (Windows) or source venv/bin/activate (Mac/Linux)
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory (copy the contents from `.env.example`). Ensure `USE_CLOUDINARY=False` is set if you don't have API keys yet.
5. Run the database migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
6. Visit `http://localhost:8000` in your browser.

### Step 2: Deploying to Render
This project includes a `render.yaml` Blueprint file, which fully automates the deployment of both the web server and the PostgreSQL database.

1. Push this code to a public GitHub repository.
2. Sign up for a free account at [Cloudinary](https://cloudinary.com) and retrieve your **Cloud Name**, **API Key**, and **API Secret**.
3. Sign up for a free account at [Render](https://render.com).
4. On the Render Dashboard, click **New +** and select **Blueprint**.
5. Connect your GitHub repository.
6. Render will automatically detect the database and web service. It will prompt you for your environment variables.
7. Paste your 3 Cloudinary keys into the empty boxes provided. (Render will automatically generate a highly secure `SECRET_KEY` for you).
8. Click **Deploy**. Render will install requirements, run migrations, and spin up your live website!

### Step 3: Accessing the Admin Panel
Once your site is live on Render, you'll want an Admin account to oversee the platform:
1. Go to your Render Dashboard, click on your Web Service, and navigate to the **Shell** tab.
2. Type the following command to create an admin user:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow the prompts to set a username, email, and password.
4. Go to your live website URL and add `/admin` to the end (e.g., `https://photo-manager.onrender.com/admin`). Log in with the credentials you just made to access the control panel!
