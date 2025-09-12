"""
Test configuration and fixtures for HRMS tests.
"""
import pytest
import tempfile
import os
from app import app, db
from config import TestingConfig


@pytest.fixture
def client():
    """Create a test client."""
    # Create a temporary database file
    db_fd, temp_db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{temp_db_path}'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()
    
    # Clean up temporary database
    os.close(db_fd)
    os.unlink(temp_db_path)


@pytest.fixture
def app_context():
    """Create an application context."""
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def authenticated_user(client):
    """Create an authenticated user session."""
    # Login with default admin user
    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    return client
