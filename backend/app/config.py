import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMES_FILE_PATH = os.path.join(BASE_DIR, "schemes_data.json")

# Security and Keys
SECRET_KEY = os.environ.get("JANMITRA_SECRET_KEY", "janmitra_super_secret_jwt_key_99182")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week

# Database
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/janmitra.db")

# Optional APIs
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
