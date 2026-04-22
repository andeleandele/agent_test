import os
os.environ["TESTING"] = "true"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from fastapi.testclient import TestClient

from main import app
from db import Base, engine
from models.users import User

# Create all tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True)
def reset_db():
    """Clear database before each test"""
    # Get a connection
    connection = engine.connect()
    # Delete all data from each table
    for table in reversed(Base.metadata.sorted_tables):
        connection.execute(table.delete())
    connection.commit()
    connection.close()
    yield

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    """Clean up test database file after all tests"""
    yield
    # Remove the test database file
    if os.path.exists("testdb.sqlite"):
        os.remove("testdb.sqlite")
