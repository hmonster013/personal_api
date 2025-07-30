# WSGI config for PythonAnywhere
# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/personal_api'  # Update with your actual path
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'personal_api.settings'

# Load environment variables from .env.production
from decouple import config
import os
from pathlib import Path

# Load .env.production file
env_path = Path(path) / '.env.production'
if env_path.exists():
    from decouple import Config, RepositoryEnv
    config = Config(RepositoryEnv(str(env_path)))
    
    # Set environment variables
    os.environ.setdefault('SECRET_KEY', config('SECRET_KEY', default=''))
    os.environ.setdefault('DEBUG', config('DEBUG', default='False'))
    os.environ.setdefault('APP_ENV', config('APP_ENV', default='production'))
    os.environ.setdefault('ALLOWED_HOSTS', config('ALLOWED_HOSTS', default=''))
    os.environ.setdefault('CORS_ALLOWED_ORIGINS', config('CORS_ALLOWED_ORIGINS', default=''))
    
    # Database settings
    os.environ.setdefault('POSTGRES_DB', config('POSTGRES_DB', default=''))
    os.environ.setdefault('POSTGRES_USER', config('POSTGRES_USER', default=''))
    os.environ.setdefault('POSTGRES_PASSWORD', config('POSTGRES_PASSWORD', default=''))
    os.environ.setdefault('POSTGRES_HOST', config('POSTGRES_HOST', default=''))
    os.environ.setdefault('POSTGRES_PORT', config('POSTGRES_PORT', default='5432'))
    
    # Cloudinary settings
    os.environ.setdefault('CLOUDINARY_CLOUD_NAME', config('CLOUDINARY_CLOUD_NAME', default=''))
    os.environ.setdefault('CLOUDINARY_API_KEY', config('CLOUDINARY_API_KEY', default=''))
    os.environ.setdefault('CLOUDINARY_API_SECRET', config('CLOUDINARY_API_SECRET', default=''))

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
