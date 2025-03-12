# SQLAlchemy/Alembic Migrations System in Pomodoro TimerFlow Project

## Overview

This document explains the database migration system built using SQLAlchemy and Alembic for the Pomodoro TimerFlow project. It covers how the migration system works, the current configuration, and how to use it to manage database schema changes.

## How Migrations Work

Database migrations track changes to your database schema over time. They allow you to:

1. **Version Control**: Track all changes to your database structure
2. **Reproducibility**: Recreate the database schema at any point in time
3. **Collaboration**: Let multiple developers work with a consistent database structure
4. **Deployment**: Safely update database schemas in production

### Key Components

The migration system consists of:

- **SQLAlchemy Models**: Defined in `backend/app/models.py` 
- **Alembic**: A migration tool designed specifically for SQLAlchemy
- **Migration Scripts**: Auto-generated files that implement database changes
- **Migration Commands**: Tools for creating and applying migrations

## Current Setup & Architecture

The migration system in this project is configured as follows:

1. **Models Layer**: SQLAlchemy models defined in `app/models.py`
2. **Database Connection**: Configuration in `app/database.py`
3. **Alembic Configuration**: Settings in `app/alembic/env.py` and `alembic.ini`
4. **Migration Scripts**: Stored in `app/alembic/versions/` 
5. **Management Script**: Custom utility in `app/manage_db.py`
6. **Docker Integration**: Scripts to run migrations within containers

## Current Challenges

The migration system is facing several issues:

1. **Path Resolution**: Difficulty accessing migration scripts in Docker container
2. **Configuration Issues**: Alembic not properly detecting model changes
3. **Container Structure**: Uncertainty about exact file paths inside containers
4. **Workflow Integration**: Need for simpler, more reliable commands

## Usage Instructions

### Prerequisites

- Docker and Docker Compose installed
- Pomodoro TimerFlow application running in Docker

### Basic Migration Commands

```bash
# Create new migrations (detecting model changes)
./backend/db_migrate.sh makemigrations "describe your changes"

# Apply pending migrations
./backend/db_migrate.sh migrate

# View migration history
./backend/db_migrate.sh showmigrations
```

### Typical Workflow

1. Make changes to your SQLAlchemy models in `app/models.py`
2. Run `./backend/db_migrate.sh makemigrations "description"` to create migration scripts
3. Inspect the generated migration in `app/alembic/versions/`
4. Apply the migration with `./backend/db_migrate.sh migrate`
5. Verify the changes in your database

## Troubleshooting

### Common Issues

- **"No module named app.manage_db"**: Path resolution issue in Docker container
- **"No such file or directory"**: Incorrect file path in Docker container
- **Empty migrations created**: Alembic configuration not detecting model changes
- **Migration errors**: Conflicts between model definitions and database state

### Debugging Steps

1. Verify container is running: `docker ps | grep pomodoro-app-container`
2. Check file paths inside container: 
   ```bash
   docker exec -it pomodoro-app-container find /app -name "manage_db.py"
   ```
3. Inspect Alembic configuration:
   ```bash
   docker exec -it pomodoro-app-container cat /app/app/alembic/env.py
   ```
4. Check if migrations are being detected:
   ```bash
   docker exec -it pomodoro-app-container python -c "from app.models import Base; print(Base.metadata.tables.keys())"
   ```

## Status
Migrations work with docker restarting