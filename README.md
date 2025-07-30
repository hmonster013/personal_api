# Personal Portfolio API
 
A comprehensive Django REST API backend for personal portfolio websites, featuring blog management, project showcases, work experiences, and contact functionality.

## 🚀 Features

### Core Modules
- **Blog Management**: Create and manage blog posts with rich text content, cover images, and skill tags
- **Project Showcase**: Display projects with descriptions, images, GitHub/website links, and technology stacks
- **Work Experience**: Manage professional experience with company details, job descriptions, and timelines
- **Contact System**: Handle contact form submissions with status tracking and admin management
- **File Management**: Integrated Cloudinary service for image and file uploads
- **Skills & Links**: Manage technical skills and social/professional links

### Technical Features
- **RESTful API**: Clean, well-documented API endpoints
- **Admin Interface**: Comprehensive Django admin for content management
- **Rich Text Editor**: CKEditor integration with code snippet support
- **Image Management**: Cloudinary integration for optimized image delivery
- **Filtering & Pagination**: Advanced filtering and pagination for all list endpoints
- **CORS Support**: Configured for frontend integration
- **Docker Support**: Containerized development and deployment

## 🛠️ Tech Stack

- **Backend**: Django 5.2, Django REST Framework
- **Database**: PostgreSQL
- **File Storage**: Cloudinary
- **Rich Text**: CKEditor
- **Containerization**: Docker & Docker Compose
- **Deployment**: PythonAnywhere ready

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL
- Cloudinary account (for file uploads)

## 🔧 Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd personal_api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   APP_ENV=development

   # Database
   POSTGRES_DB=personaldb
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your-password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432

   # Cloudinary
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret

   # CORS
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4200
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### Docker Development

1. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Run migrations**
   ```bash
   docker-compose exec api python manage.py migrate
   docker-compose exec api python manage.py createsuperuser
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/v1/
```

### Endpoints

#### Common
- `GET /v1/all-configs` - Get system configurations
- `GET /v1/skills/list` - List all skills
- `GET /v1/links/list` - List all links
- `GET /v1/links/view/<name>` - Get link details
- `POST /v1/contacts/create` - Create contact submission

#### Blog Management
- `GET /v1/blogs/list` - List all blogs
- `GET /v1/blogs/view/<id>` - Get blog details

#### Projects
- `GET /v1/projects/list` - List all projects
- `GET /v1/projects/view/<id>` - Get project details

#### Experiences
- `GET /v1/experiences/list` - List all experiences
- `GET /v1/experiences/view/<id>` - Get experience details

### Sample API Calls

#### Create Contact
```bash
curl -X POST http://localhost:8000/v1/contacts/create \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "subject": "Inquiry about services",
    "message": "I would like to know more about your services."
  }'
```

#### Get Blogs
```bash
curl http://localhost:8000/v1/blogs/list
```

## 🗄️ Database Schema

### Core Models

#### Blog
- Title, content (rich text), description
- Cover image, publication status
- Associated skills and creation timestamps

#### Project
- Name, description, project images
- GitHub and website links
- Technology stack (skills)

#### Experience
- Company information and logo
- Job title, description, working period
- Join and leave dates

#### Contact
- Contact information (name, email, subject, message)
- Status tracking (NEW, READ, REPLIED, CLOSED)
- IP address and user agent logging
- Admin notes and response tracking

## 🔐 Admin Interface

Access the Django admin at `http://localhost:8000/admin/`

### Features
- **Content Management**: Full CRUD operations for all models
- **Rich Text Editing**: CKEditor integration for blog posts and descriptions
- **Image Management**: Upload and manage images through Cloudinary
- **Contact Management**: Track and respond to contact submissions
- **User Management**: Admin user management and permissions

## 🚀 Deployment

### PythonAnywhere Deployment

1. **Upload code to PythonAnywhere**
2. **Install dependencies**
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
3. **Configure environment variables**
4. **Set up WSGI configuration**
5. **Run migrations and collect static files**
   ```bash
   python3.10 manage.py migrate
   python3.10 manage.py collectstatic --noinput
   ```

Detailed deployment instructions are available in `DEPLOYMENT.md`.

## 📁 Project Structure

```
personal_api/
├── authentication/          # Authentication app (future use)
├── common/                 # Common models and utilities
│   ├── models.py          # File, Links, Skills, Contact models
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   └── admin.py           # Admin configurations
├── info/                  # Information management
│   ├── models.py          # Blog, Project, Experience models
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   └── admin.py           # Admin configurations
├── personal/              # Personal app (future use)
├── configs/               # Configuration files
├── helpers/               # Helper utilities
├── utils/                 # Utility functions
├── personal_api/          # Main Django project
│   ├── settings.py        # Django settings
│   └── urls.py            # URL configurations
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker configuration
├── Dockerfile            # Docker image configuration
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions, please use the contact form through the API or reach out through the configured contact methods.
# Personal Portfolio API

A comprehensive Django REST API backend for personal portfolio websites, featuring blog management, project showcases, work experiences, and contact functionality.

## 🚀 Features

### Core Modules
- **Blog Management**: Create and manage blog posts with rich text content, cover images, and skill tags
- **Project Showcase**: Display projects with descriptions, images, GitHub/website links, and technology stacks
- **Work Experience**: Manage professional experience with company details, job descriptions, and timelines
- **Contact System**: Handle contact form submissions with status tracking and admin management
- **File Management**: Integrated Cloudinary service for image and file uploads
- **Skills & Links**: Manage technical skills and social/professional links

### Technical Features
- **RESTful API**: Clean, well-documented API endpoints
- **Admin Interface**: Comprehensive Django admin for content management
- **Rich Text Editor**: CKEditor integration with code snippet support
- **Image Management**: Cloudinary integration for optimized image delivery
- **Filtering & Pagination**: Advanced filtering and pagination for all list endpoints
- **CORS Support**: Configured for frontend integration
- **Docker Support**: Containerized development and deployment

## 🛠️ Tech Stack

- **Backend**: Django 5.2, Django REST Framework
- **Database**: PostgreSQL
- **File Storage**: Cloudinary
- **Rich Text**: CKEditor
- **Containerization**: Docker & Docker Compose
- **Deployment**: PythonAnywhere ready

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL
- Cloudinary account (for file uploads)

## 🔧 Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd personal_api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   APP_ENV=development

   # Database
   POSTGRES_DB=personaldb
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your-password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432

   # Cloudinary
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret

   # CORS
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4200
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### Docker Development

1. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Run migrations**
   ```bash
   docker-compose exec api python manage.py migrate
   docker-compose exec api python manage.py createsuperuser
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/v1/
```

### Endpoints

#### Common
- `GET /v1/all-configs` - Get system configurations
- `GET /v1/skills/list` - List all skills
- `GET /v1/links/list` - List all links
- `GET /v1/links/view/<name>` - Get link details
- `POST /v1/contacts/create` - Create contact submission

#### Blog Management
- `GET /v1/blogs/list` - List all blogs
- `GET /v1/blogs/view/<id>` - Get blog details

#### Projects
- `GET /v1/projects/list` - List all projects
- `GET /v1/projects/view/<id>` - Get project details

#### Experiences
- `GET /v1/experiences/list` - List all experiences
- `GET /v1/experiences/view/<id>` - Get experience details

### Sample API Calls

#### Create Contact
```bash
curl -X POST http://localhost:8000/v1/contacts/create \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "subject": "Inquiry about services",
    "message": "I would like to know more about your services."
  }'
```

#### Get Blogs
```bash
curl http://localhost:8000/v1/blogs/list
```

## 🗄️ Database Schema

### Core Models

#### Blog
- Title, content (rich text), description
- Cover image, publication status
- Associated skills and creation timestamps

#### Project
- Name, description, project images
- GitHub and website links
- Technology stack (skills)

#### Experience
- Company information and logo
- Job title, description, working period
- Join and leave dates

#### Contact
- Contact information (name, email, subject, message)
- Status tracking (NEW, READ, REPLIED, CLOSED)
- IP address and user agent logging
- Admin notes and response tracking

## 🔐 Admin Interface

Access the Django admin at `http://localhost:8000/admin/`

### Features
- **Content Management**: Full CRUD operations for all models
- **Rich Text Editing**: CKEditor integration for blog posts and descriptions
- **Image Management**: Upload and manage images through Cloudinary
- **Contact Management**: Track and respond to contact submissions
- **User Management**: Admin user management and permissions

## 🚀 Deployment

### PythonAnywhere Deployment

1. **Upload code to PythonAnywhere**
2. **Install dependencies**
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
3. **Configure environment variables**
4. **Set up WSGI configuration**
5. **Run migrations and collect static files**
   ```bash
   python3.10 manage.py migrate
   python3.10 manage.py collectstatic --noinput
   ```

Detailed deployment instructions are available in `DEPLOYMENT.md`.

## 📁 Project Structure

```
personal_api/
├── authentication/          # Authentication app (future use)
├── common/                 # Common models and utilities
│   ├── models.py          # File, Links, Skills, Contact models
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   └── admin.py           # Admin configurations
├── info/                  # Information management
│   ├── models.py          # Blog, Project, Experience models
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   └── admin.py           # Admin configurations
├── personal/              # Personal app (future use)
├── configs/               # Configuration files
├── helpers/               # Helper utilities
├── utils/                 # Utility functions
├── personal_api/          # Main Django project
│   ├── settings.py        # Django settings
│   └── urls.py            # URL configurations
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker configuration
├── Dockerfile            # Docker image configuration
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions, please use the contact form through the API or reach out through the configured contact methods.