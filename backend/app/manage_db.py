# backend/app/manage_db.py

import os
import sys
import argparse
from alembic.config import Config
from alembic import command

def get_alembic_config():
    # Adjust path to find alembic.ini inside the app directory
    alembic_ini = os.path.join("/app/app", "alembic.ini")
    
    # Create Alembic config
    alembic_cfg = Config(alembic_ini)
    
    # Set scripts location
    script_location = os.path.join("/app/app", "alembic")
    alembic_cfg.set_main_option("script_location", script_location)
    
    return alembic_cfg

def create_migration(message):
    """Create a new migration with auto-detection of changes"""
    alembic_cfg = get_alembic_config()
    command.revision(alembic_cfg, autogenerate=True, message=message)
    print(f"Migration created with message: {message}")

def apply_migrations():
    """Apply all pending migrations"""
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, "head")
    print("Migrations applied successfully")

def show_migrations():
    """Show migration history"""
    alembic_cfg = get_alembic_config()
    command.history(alembic_cfg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database migration manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create migrations command
    create_parser = subparsers.add_parser("makemigrations", help="Create new migration")
    create_parser.add_argument("message", help="Migration message")
    
    # Apply migrations command
    migrate_parser = subparsers.add_parser("migrate", help="Apply migrations")
    
    # Show migrations command
    history_parser = subparsers.add_parser("showmigrations", help="Show migration history")
    
    args = parser.parse_args()
    
    if args.command == "makemigrations":
        create_migration(args.message)
    elif args.command == "migrate":
        apply_migrations()
    elif args.command == "showmigrations":
        show_migrations()
    else:
        parser.print_help()