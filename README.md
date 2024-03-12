# TODO List API

A RESTful API to create and manage TODO lists with FastAPI, PostgreSQL, Docker, and Docker Compose, featuring CI/CD with GitHub Actions.

## Features

- Create TODO lists with names.
- Add TODO items with optional deadlines.
- View TODO lists and items.
- [TODO] Search TODO lists with case-insensitive text.
- 
## How to Use

1. Create a Todo List
This example creates a new todo list with the name "Grocery Shopping" and includes two items in the list.

```
curl -X 'POST' \
  'http://localhost:8000/todo/list/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Grocery Shopping",
  "items": [
    {
      "title": "Buy milk",
      "deadline": "2024-04-01T09:00:00"
    },
    {
      "title": "Buy eggs",
      "deadline": "2024-04-01T10:00:00"
    }
  ]
}'

```

3. Read a Specific Todo List
This retrieves the items of a specific todo list by its list_id. Replace :list_id with the actual ID of the list you want to retrieve.

```
curl -X 'GET' \
  'http://localhost:8000/todo/list/:list_id/' \
  -H 'accept: application/json'
```

4. Add an Item to a Todo List
This adds a new item to an existing todo list. Replace :list_id with the ID of the list you want to add an item to.

```
curl -X 'POST' \
  'http://localhost:8000/todo/list/:list_id/item/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Buy bread",
  "deadline": "2024-04-02T12:00:00"
}'
```



## Prerequisites

- Docker
- Docker Compose
- Python 3.9+

## Local Setup

1. **Clone the Repository**
``` 
git clone https://github.com/adilnaut/todo-list
cd https://github.com/adilnaut/todo-list
```
 
2. **Environment Variables**
Create a `.env` file in the root directory with the following content:

DATABASE_URL=postgresql://your_db_user:your_pass@db:your_port/your_db_name
TEST_DATABASE_URL=postgresql://your_db_user:your_pass@db:your_port/your_db_name_test

3. **Start the Application with Docker Compose**

```
docker-compose up --build
```

The API will be accessible at `http://localhost:8000`.

4. **Running Migrations**

Before the first run, you might need to apply database migrations:

```
docker-compose exec web python -m app.alembic_utils alembic_upgrade_to_head
```

or (first edit comment for migration)

```
python manage_alembic.py 
```

## Testing

Run tests locally by executing:

```
docker-compose exec web pytest
```



## CI/CD with GitHub Actions (Work in Progress - consider it as a separate experimental branch) 

This repository is configured with GitHub Actions for continuous integration and deployment.

### Continuous Integration

On every push, the `.github/workflows/python-application.yml` workflow is triggered to install dependencies, run tests, and ensure the code meets our standards.

### Deployment to Production

The `.github/workflows/deployment.yml` workflow is triggered on pushes to the `main` branch. It builds the Docker image, pushes it to Docker Hub, and deploys it to a production server.

## Deployment Instructions

### Server Preparation

Ensure your Ubuntu/Debian server has Docker and Docker Compose installed.

### GitHub Secrets

Set the following secrets in your GitHub repository:

- `DOCKER_USERNAME` and `DOCKER_PASSWORD` for Docker Hub authentication.
- `SERVER_HOST`, `SERVER_USER`, and `SERVER_SSH_KEY` for SSH access to your production server.

### Deployment Workflow

The deployment workflow will:

1. Build and push the Docker image to Docker Hub.
2. SSH into your production server.
3. Pull the latest Docker image.
4. Deploy the application using Docker Compose.

Refer to `.github/workflows/deployment.yml` for the workflow configuration.


