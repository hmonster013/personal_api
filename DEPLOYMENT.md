# Deployment Guide

## Local Development Setup

1. **Update .env file:**
   - File `.env` đã có sẵn với cấu hình local
   - Kiểm tra và cập nhật thông tin database nếu cần
   - Cloudinary credentials đã được điền sẵn

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

## Production Deployment on PythonAnywhere

### 1. Upload Code
- Upload your project to PythonAnywhere
- Recommended path: `/home/yourusername/personal_api`

### 2. Install Dependencies
```bash
# In PythonAnywhere console
cd ~/personal_api
pip3.10 install --user -r requirements.txt
```

### 3. Configure Environment
- Update `.env.production` with your settings:
  - `SECRET_KEY` - Generate strong random key
  - `ALLOWED_HOSTS` - Your PythonAnywhere domain
  - Database settings (Supabase đã cấu hình sẵn)

### 4. Setup Web App
- Go to Web tab in PythonAnywhere dashboard
- Create new web app (Django)
- Set WSGI file path: `/home/yourusername/personal_api/wsgi_pythonanywhere.py`
- Update path in `wsgi_pythonanywhere.py` to match your actual path

### 5. Static Files
```bash
# Collect static files
python3.10 manage.py collectstatic --noinput
```

### 6. Database Migration
```bash
# Run migrations
python3.10 manage.py migrate
```

### 7. Reload Web App
- Click "Reload" button in Web tab

## Files Structure

- `.env` - Local development environment (đã cấu hình)
- `.env.production` - Production environment (PythonAnywhere)
- `wsgi_pythonanywhere.py` - WSGI configuration cho PythonAnywhere
- `requirements.txt` - Python dependencies
- `DEPLOYMENT.md` - Hướng dẫn deploy
