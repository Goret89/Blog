# Django Blog Project

A simple Django blog project running in Docker with PostgreSQL.

---

## Project Structure

Blog/
├── blog_project/
│ ├── blog/ # Django app
│ ├── blog_project/ # Django project settings
│ └── manage.py # Django CLI
├── Dockerfile # App Dockerfile
├── docker-compose.yml # Docker Compose config

---

## Launch in Docker

### Build and Start the Application

1. Make sure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is running.
2. From the project root (`Blog/`), run:

```bash
docker-compose up --build

## Application Tasks

### Run Migrations

```bash
docker-compose run web python manage.py migrate

### Create Superuser

```bash
docker-compose run web python manage.py createsuperuser

### Access the Application
1. App: http://localhost:8000
2. Admin Panel: http://localhost:8000/admin/

## Reset Database

### Stop and Remove Containers and Volumes

```bash
docker-compose down -v

Note: This will delete all database data, since volumes will be removed.

### Rebuild and Start the App Again

```bash
docker-compose up --build