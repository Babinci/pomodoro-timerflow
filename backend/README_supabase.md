# Pomodoro TimerFlow Supabase Migration

This document provides instructions for migrating the Pomodoro TimerFlow application from SQLite/SQLAlchemy to Supabase.

## Overview

The migration involves:

1. Setting up Supabase tables and row-level security policies
2. Replacing authentication with Supabase Auth
3. Updating data access operations to use Supabase client
4. Integrating with existing WebSocket functionality

## Migration Steps

### 1. Install Dependencies

```bash
pip install -r requirements_supabase.txt
```

### 2. Environment Setup

Create a `.env` file in the `/app` directory with the following variables:

```
SUPABASE_URL=https://your-project-url.supabase.co
SUPABASE_KEY=your-supabase-key
```

### 3. Database Migration

The database tables have been created in the Supabase schema:

- `users`: User accounts and settings
- `tasks`: User tasks with ordering
- `pomodoro_sessions`: Session tracking
- `pomodoro_checkpoints`: Timer state preservation

### 4. Authentication Migration

Authentication is now handled by Supabase Auth:

- User registration uses Supabase Auth sign-up
- Login uses Supabase Auth sign-in
- JWT tokens are managed by Supabase
- User metadata is stored in both Auth and the database

### 5. Switching to Supabase Implementation

To use the Supabase implementation:

1. Update the Docker container entrypoint to use `main_supabase.py` instead of `main.py`
2. Make sure your environment variables are correctly set
3. Run the updated application

## Usage

### Development Testing

For local development and testing with Supabase:

1. Set up a local Supabase instance using Docker
2. Update your environment variables to point to the local instance
3. Run the FastAPI server with:

```bash
uvicorn app.main_supabase:app --reload
```

### Production Deployment

For production deployment:

1. Update the Dockerfile to use the Supabase implementation:

```dockerfile
# Change this line
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]

# To this
CMD ["uvicorn", "app.main_supabase:app", "--host", "0.0.0.0", "--port", "8003"]
```

2. Set your Supabase production environment variables
3. Build and deploy the Docker container

## Troubleshooting

### Common Issues

1. **Authentication failures**: Check that your Supabase URL and API key are correct
2. **Database permission errors**: Verify Row Level Security (RLS) policies are correctly set up
3. **WebSocket connection issues**: The WebSocket implementation still uses the original code, so ensure compatibility

### Fallback Plan

If issues occur, you can revert to the SQLite implementation by:

1. Using the original `main.py` instead of `main_supabase.py`
2. Using the original dependencies instead of the Supabase client

## References

- [Supabase Python Client Documentation](https://supabase.com/docs/reference/python)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Original Pomodoro TimerFlow Documentation](../README.md)
