import os
import subprocess
from pathlib import Path


SQLALCHEMY_DATABASE_URL = "postgresql://todolist_user:1234@localhost:5433/tododb"
ALEMBIC_CONFIG_PATH = "alembic.ini"

def initialize_alembic():
    # Initialize Alembic
    subprocess.run(["alembic", "init", "alembic"], check=True)

    # Update alembic.ini with SQLALCHEMY_DATABASE_URL
    alembic_ini_path = Path(ALEMBIC_CONFIG_PATH)
    assert alembic_ini_path.is_file(), f"{ALEMBIC_CONFIG_PATH} not found."

    with open(alembic_ini_path, "r") as file:
        data = file.readlines()

    with open(alembic_ini_path, "w") as file:
        for line in data:
            if line.startswith("sqlalchemy.url ="):
                file.write(f"sqlalchemy.url = {SQLALCHEMY_DATABASE_URL}\n")
            else:
                file.write(line)

def update_env_py():
    # Modify env.py to include your models for autogeneration
    env_path = Path("alembic/env.py")
    assert env_path.is_file(), "alembic/env.py not found."

    with open(env_path, "a") as file:
        file.write("\nfrom app.db.database import Base\nfrom app.models.models import *\n")
        file.write("target_metadata = Base.metadata\n")

def create_migration(message="initial migration"):
    # Create a new migration
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message], check=True)

def upgrade_database():
    # Apply migrations to the database
    subprocess.run(["alembic", "upgrade", "head"], check=True)

if __name__ == "__main__":
    initialize_alembic()
    update_env_py()
    create_migration()
    upgrade_database()
