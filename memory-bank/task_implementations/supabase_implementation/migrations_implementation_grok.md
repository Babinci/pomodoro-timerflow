# Migration Implementation Plan for Pomodoro TimerFlow with Supabase

This document outlines a comprehensive plan to migrate the existing SQLite database in the Pomodoro TimerFlow project to Supabase (PostgreSQL-based) while maintaining a Django-like migration workflow. The goal is to ensure that the tables match those defined in `backend/app/models.py` and to enable easy management of schema changes (e.g., adding new tables or fields) using SQLAlchemy and Alembic.

---

## Objectives
- **Migrate Database**: Transition from SQLite to Supabase's PostgreSQL database.
- **Preserve Schema**: Ensure tables align with `models.py` (e.g., `users`, `tasks`, `pomodoro_sessions`, `pomodoro_checkpoints`).
- **Simplify Migrations**: Implement an easy-to-use migration system similar to Django's `makemigrations` and `migrate` commands.
- **Support Future Changes**: Allow seamless addition of new tables and fields.

---

## Current Setup Overview
- **Database**: SQLite (`sqlite:////app/db/pomodoro.db`) defined in `backend/app/database.py`.
- **ORM**: SQLAlchemy with models in `backend/app/models.py`.
- **Migration Tool**: Alembic configured in `backend/app/alembic/` with scripts in `versions/`.
- **Management**: Custom script `backend/app/manage_db.py` and shell script `backend/db_migrate.sh` for migration commands.
- **Environment**: Dockerized FastAPI application with `.env` file for configuration.

---

## Migration Plan

### Step 1: Update Database Connection to Supabase
#### Objective
Switch the database connection from SQLite to Supabase's PostgreSQL instance using environment variables for flexibility.

#### Actions
1. **Obtain Supabase Connection String**:
   - From your Supabase project dashboard, get the PostgreSQL connection string:
     ```
     postgresql://[user]:[password]@[host]:[port]/[dbname]
     ```
   - For local development, use the Supabase CLI (`npx supabase start`) to get a local string, e.g.:
     ```
     postgresql://postgres:postgres@localhost:54322/postgres
     ```

2. **Update `database.py`**:
   - Modify `backend/app/database.py` to read the database URL from an environment variable with a fallback to SQLite:
     ```python
     import os
     from sqlalchemy import create_engine
     from sqlalchemy.ext.declarative import declarative_base
     from sqlalchemy.orm import sessionmaker

     SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////app/db/pomodoro.db")

     engine = create_engine(
         SQLALCHEMY_DATABASE_URL,
         connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
     )

     Base = declarative_base()

     # Import models to register with Base
     from . import models

     Base.metadata.create_all(bind=engine)

     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

     def get_db():
         db = SessionLocal()
         try:
             yield db
         finally:
             db.close()
     ```

3. **Configure `.env` File**:
   - Update `backend/credentials/.env` with the Supabase connection string:
     ```
     DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres
     ```
   - For production, replace with the remote Supabase URL.

4. **Verify Docker Configuration**:
   - The Dockerfile copies `.env` to `/app/.env`, and `auth.py` loads it using `load_dotenv("/app/.env")`. Ensure the `.env` file is correctly mounted in `restart_docker.sh`:
     ```bash
     docker run -d -p 8003:8003 \
       -v $(pwd)/db_local:/app/db \
       -v $(pwd)/logs:/app/logs \
       -v $(pwd)/backend/credentials/.env:/app/.env \
       --name pomodoro-app-container pomodoro-app
     ```

---

### Step 2: Ensure Model Compatibility with PostgreSQL
#### Objective
Confirm that the SQLAlchemy models in `models.py` work with PostgreSQL, leveraging features like `JSONB` where beneficial.

#### Actions
1. **Review Current Models**:
   - Current models (`users`, `tasks`, `pomodoro_sessions`, `pomodoro_checkpoints`) use standard types: `Integer`, `String`, `DateTime`, `JSON`, `Boolean`, `ForeignKey`.
   - Example from `models.py`:
     ```python
     class User(Base):
         __tablename__ = "users"
         id = Column(Integer, primary_key=True, index=True)
         email = Column(String, unique=True, index=True)
         username = Column(String, unique=True, index=True)
         hashed_password = Column(String)
         pomodoro_settings = Column(JSON, default={...})
     ```

2. **Optimize for PostgreSQL**:
   - The `JSON` type for `pomodoro_settings` maps to `JSONB` in PostgreSQL by default in SQLAlchemy (since version 1.1), which is more efficient. No changes are needed:
     ```python
     pomodoro_settings = Column(JSON, default={...})
     ```
   - Other types (e.g., `Integer`, `String`) are fully compatible.

3. **Test Compatibility**:
   - No SQLite-specific features (e.g., `check_same_thread`) are relied upon beyond the connection args, which are conditionally applied.

---

### Step 3: Configure Alembic for Supabase
#### Objective
Ensure Alembic connects to the Supabase database and can generate and apply migrations.

#### Actions
1. **Verify `env.py`**:
   - `backend/app/alembic/env.py` already uses `SQLALCHEMY_DATABASE_URL` from `database.py`:
     ```python
     from app.database import SQLALCHEMY_DATABASE_URL
     config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
     ```
   - No changes needed as it dynamically adopts the `.env` configuration.

2. **Update `alembic.ini`** (Optional):
   - The default `sqlalchemy.url` in `alembic.ini` is a placeholder. Since `env.py` overrides it, no update is required:
     ```
     sqlalchemy.url = driver://user:pass@localhost/dbname
     ```

3. **Test Connection**:
   - Start the Supabase local instance:
     ```bash
     npx supabase start
     ```
   - Run a test command inside the container to ensure connectivity:
     ```bash
     docker exec -it pomodoro-app-container python -c "from app.database import engine; engine.connect()"
     ```

---

### Step 4: Generate and Apply Initial Migration
#### Objective
Create the initial database schema in Supabase based on `models.py`.

#### Actions
1. **Reset Supabase Database** (if needed):
   - For a fresh start, stop and restart the local Supabase instance to clear existing data:
     ```bash
     npx supabase stop
     npx supabase start
     ```

2. **Generate Initial Migration**:
   - Run the `makemigrations` command to autogenerate a migration script:
     ```bash
     ./backend/db_migrate.sh makemigrations "Initial migration to Supabase"
     ```
   - This creates a file in `backend/app/alembic/versions/` (e.g., `xxxx_initial_migration_to_supabase.py`).

3. **Review Migration Script**:
   - Check the generated script to ensure it creates all tables (`users`, `tasks`, `pomodoro_sessions`, `pomodoro_checkpoints`) as defined in `models.py`. Example snippet:
     ```python
     def upgrade():
         op.create_table('users',
             sa.Column('id', sa.Integer(), nullable=False),
             sa.Column('email', sa.String(), nullable=True),
             sa.Column('username', sa.String(), nullable=True),
             sa.Column('hashed_password', sa.String(), nullable=True),
             sa.Column('pomodoro_settings', sa.JSON(), nullable=True),
             sa.PrimaryKeyConstraint('id')
         )
         # Other tables...
     ```

4. **Apply Migration**:
   - Apply the migration to the Supabase database:
     ```bash
     ./backend/db_migrate.sh migrate
     ```

5. **Verify Tables**:
   - Use a PostgreSQL client (e.g., `psql`) or Supabase dashboard to confirm the tables exist with the correct schema.

---

### Step 5: Handle Future Schema Changes
#### Objective
Establish a workflow for adding new tables or fields, similar to Django.

#### Actions
1. **Modify Models**:
   - Example: Add a new `priority` field to the `Task` model:
     ```python
     class Task(Base):
         __tablename__ = "tasks"
         id = Column(Integer, primary_key=True, index=True)
         title = Column(String)
         description = Column(String, nullable=True)
         user_id = Column(Integer, ForeignKey("users.id"))
         estimated_pomodoros = Column(Integer)
         completed_pomodoros = Column(Integer, default=0)
         created_at = Column(DateTime, default=datetime.utcnow)
         completed_at = Column(DateTime, nullable=True)
         is_active = Column(Boolean, default=True)
         position = Column(Integer, default=999999)
         priority = Column(Integer, default=0, nullable=True)  # New field
     ```

2. **Generate Migration**:
   - Create a new migration script:
     ```bash
     ./backend/db_migrate.sh makemigrations "Add priority field to Task"
     ```
   - Review the generated script (e.g., `backend/app/alembic/versions/xxxx_add_priority_field_to_task.py`):
     ```python
     def upgrade():
         op.add_column('tasks', sa.Column('priority', sa.Integer(), nullable=True, default=0))

     def downgrade():
         op.drop_column('tasks', 'priority')
     ```

3. **Apply Migration**:
   - Apply the change:
     ```bash
     ./backend/db_migrate.sh migrate
     ```

4. **Test Application**:
   - Restart the Docker container and test endpoints (e.g., task creation) to ensure the new field is functional:
     ```bash
     ./restart_docker.sh
     ```

---

### Step 6: Data Migration (Optional)
#### Objective
Transfer existing SQLite data to Supabase, if required.

#### Actions
1. **Export SQLite Data**:
   - Use a script to dump data from SQLite:
     ```python
     from sqlalchemy import create_engine
     from app.models import Base
     import json

     sqlite_engine = create_engine("sqlite:////app/db/pomodoro.db")
     sqlite_session = sessionmaker(bind=sqlite_engine)()
     users = sqlite_session.query(User).all()
     with open("users.json", "w") as f:
         json.dump([u.__dict__ for u in users], f)
     ```

2. **Import to Supabase**:
   - Load data into Supabase:
     ```python
     supabase_engine = create_engine(os.getenv("DATABASE_URL"))
     supabase_session = sessionmaker(bind=supabase_engine)()
     with open("users.json", "r") as f:
         users_data = json.load(f)
         for user_data in users_data:
             user = User(**user_data)
             supabase_session.add(user)
         supabase_session.commit()
     ```

3. **Automate**:
   - Add this as a one-time command in `manage_db.py` if needed.

---

### Step 7: Testing and Validation
#### Objective
Ensure the application works seamlessly with Supabase.

#### Actions
1. **Restart Docker**:
   - ```bash
     ./restart_docker.sh
     ```

2. **Run Tests**:
   - Execute pytest to validate functionality:
     ```bash
     docker exec -it pomodoro-app-container pytest /app/tests
     ```

3. **Manual Testing**:
   - Test user creation, task management, and Pomodoro sessions via the web app.

---

## Final Workflow
- **Add/Modify Tables or Fields**:
  1. Update `models.py`.
  2. Run `./backend/db_migrate.sh makemigrations "message"`.
  3. Run `./backend/db_migrate.sh migrate`.
- **View History**:
  - `./backend/db_migrate.sh showmigrations`

This mirrors Django’s workflow, making schema management intuitive and efficient.

---

## Additional Considerations
- **Supabase Features**: Post-migration, explore Supabase auth and real-time capabilities (future steps).
- **Backup**: Regularly back up the Supabase database during development.
- **Documentation**: Update `memory-bank/models_migrations.md` with this plan.

This plan ensures a robust migration to Supabase while maintaining an easy-to-use system for future schema changes.