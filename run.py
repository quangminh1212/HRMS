#!/usr/bin/env python3
"""
Application entry point for HRMS.

This module provides the main entry point for running the HRMS application.
It includes proper logging setup, error handling, and environment configuration.
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

from app import app, db
from config import config


def setup_logging(app):
    """Set up application logging."""
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Set up file handler with rotation
        file_handler = RotatingFileHandler(
            'logs/hrms.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('HRMS startup')


def create_admin_user():
    """Create default admin user if it doesn't exist."""
    from models import User
    
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@hrms.local',
            role='admin'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("✓ Default admin user created (admin/admin123)")


def initialize_database():
    """Initialize database with tables and default data."""
    with app.app_context():
        # Create tables
        db.create_all()
        print("✓ Database tables created")
        
        # Create admin user
        create_admin_user()


def main():
    """Main application entry point."""
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Configure the app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Set up logging
    setup_logging(app)
    
    # Initialize database
    initialize_database()
    
    # Print startup information
    print("=" * 60)
    print("🚀 HRMS - Human Resource Management System")
    print("=" * 60)
    print(f"Environment: {config_name}")
    print(f"Debug mode: {app.debug}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("📝 Default login credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("=" * 60)
    print("🌐 Access the application at:")
    print("   http://localhost:5000")
    print("   http://127.0.0.1:5000")
    print("=" * 60)
    print("⚠️  Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run the application
    try:
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=app.debug
        )
    except KeyboardInterrupt:
        print("\n👋 HRMS server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting HRMS: {e}")
        app.logger.error(f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
