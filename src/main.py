import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from routers import user

from db import Base, engine

app = FastAPI()

# Initialize tables on app import
# (tables will be created in test conftest as well for testing)
Base.metadata.create_all(bind=engine)

app.include_router(user.router)