"""
Local development setup script
Run this to set up the development environment
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command and report status"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with error: {e}")
        return False

def main():
    """Run setup steps"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "📸 Photo Album Manager - Setup" + " "*17 + "║")
    print("╚" + "="*58 + "╝")
    
    base_dir = Path(__file__).resolve().parent
    
    # Step 1: Create .env file
    env_file = base_dir / '.env'
    env_example = base_dir / '.env.example'
    
    if not env_file.exists() and env_example.exists():
        print(f"\n⚙️  Creating .env file from template...")
        subprocess.run(f"cp {env_example} {env_file}", shell=True)
        print(f"✅ Created .env file. Please update it with your settings.")
    
    # Step 2: Run migrations
    if run_command(
        f"{sys.executable} {base_dir}/manage.py migrate",
        "Running database migrations"
    ):
        print("✅ Database migrations completed")
    
    # Step 3: Create superuser
    print(f"\n{'='*60}")
    print("▶ Creating superuser")
    print(f"{'='*60}")
    print("Creating a superuser account for admin access...")
    os.system(f"{sys.executable} {base_dir}/manage.py createsuperuser")
    
    # Step 4: Collect static files
    if run_command(
        f"{sys.executable} {base_dir}/manage.py collectstatic --noinput",
        "Collecting static files"
    ):
        print("✅ Static files collected")
    
    print(f"\n\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "✨ Setup Complete! ✨" + " "*20 + "║")
    print("╚" + "="*58 + "╝")
    print(f"\n📝 Next steps:")
    print(f"  1. Update .env with your settings (Cloudinary, Database, etc.)")
    print(f"  2. Run: python manage.py runserver")
    print(f"  3. Visit: http://localhost:8000")
    print(f"  4. Admin: http://localhost:8000/admin/")
    print(f"\n💡 Tip: Keep the development server running while you develop!\n")

if __name__ == '__main__':
    main()
