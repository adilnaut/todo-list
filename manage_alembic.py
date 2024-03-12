from alembic.config import Config
from alembic import command
from app.db.database import SQLALCHEMY_DATABASE_URL, Base  # Adjust the import as necessary
import os

# Set the base directory where 'alembic' folder is located
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def get_alembic_config():
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", os.path.join(BASE_DIR, "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    return alembic_cfg

def alembic_upgrade_to_head():
    """Upgrade the database to the latest revision."""
    config = get_alembic_config()
    command.upgrade(config, "head")

def alembic_revision(message="create initial tables", autogenerate=True):
    """Create a new revision."""
    config = get_alembic_config()
    command.revision(config, message=message, autogenerate=autogenerate)

if __name__ == "__main__":
    # Example usage: Create a new revision and upgrade to it
    alembic_revision("Initial database setup", autogenerate=True)
    alembic_upgrade_to_head()
