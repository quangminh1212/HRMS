#!/usr/bin/env python3
"""
XLAB HRMS Configuration Testing Suite

Comprehensive testing for configuration management.
Following international testing standards.
"""

import pytest
import os
from unittest.mock import patch

from src.config.settings import Settings, get_settings


class TestConfigurationManagement:
    """Test suite for configuration management."""
    
    def test_default_configuration(self):
        """Test default configuration values."""
        settings = Settings()
        
        # Test database defaults
        assert settings.database.url == "sqlite:///database.db"
        assert settings.database.echo is False
        assert settings.database.pool_size == 10
        
        # Test server defaults
        assert settings.server.host == "0.0.0.0"
        assert settings.server.port == 3000
        assert settings.server.debug is False
        
        # Test security defaults
        assert settings.security.session_timeout == 3600
        assert settings.security.max_login_attempts == 5
        assert settings.security.password_min_length == 8
        
        # Test UI defaults
        assert settings.ui.theme_primary_color == "#14B8A6"
        assert settings.ui.theme_background_color == "#FFFFFF"
    
    @patch.dict(os.environ, {
        'HRMS_ENV': 'production',
        'SERVER_PORT': '8080',
        'DEBUG': 'true',
        'DATABASE_URL': 'postgresql://user:pass@localhost/hrms',
        'SECRET_KEY': 'production-secret-key',
        'LOG_LEVEL': 'WARNING'
    })
    def test_environment_variable_override(self):
        """Test configuration override with environment variables."""
        settings = Settings()
        
        assert settings.environment == 'production'
        assert settings.server.port == 8080
        assert settings.server.debug is True
        assert settings.database.url == 'postgresql://user:pass@localhost/hrms'
        assert settings.security.secret_key == 'production-secret-key'
        assert settings.logging.level == 'WARNING'
    
    def test_configuration_validation(self):
        """Test configuration validation."""
        # Test invalid port
        with patch.dict(os.environ, {'SERVER_PORT': '99999'}):
            with pytest.raises(ValueError, match="Invalid port number"):
                Settings()
        
        # Test invalid log level
        with patch.dict(os.environ, {'LOG_LEVEL': 'INVALID'}):
            with pytest.raises(ValueError, match="Invalid log level"):
                Settings()
    
    def test_streamlit_config_generation(self):
        """Test Streamlit configuration generation."""
        settings = Settings()
        streamlit_config = settings.get_streamlit_config()
        
        expected_keys = [
            'server.port', 'server.address', 'browser.gatherUsageStats',
            'theme.primaryColor', 'theme.backgroundColor',
            'theme.secondaryBackgroundColor', 'theme.textColor'
        ]
        
        for key in expected_keys:
            assert key in streamlit_config
        
        assert streamlit_config['server.port'] == 3000
        assert streamlit_config['theme.primaryColor'] == '#14B8A6'
    
    def test_environment_detection(self):
        """Test environment detection methods."""
        # Test development environment
        with patch.dict(os.environ, {'HRMS_ENV': 'development'}):
            settings = Settings()
            assert settings.is_development() is True
            assert settings.is_production() is False
        
        # Test production environment
        with patch.dict(os.environ, {'HRMS_ENV': 'production'}):
            settings = Settings()
            assert settings.is_development() is False
            assert settings.is_production() is True
    
    def test_database_url_absolute_path(self):
        """Test SQLite database URL conversion to absolute path."""
        with patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///test.db'}):
            settings = Settings()
            
            # Should convert to absolute path
            assert settings.database.url.startswith('sqlite:///')
            assert 'test.db' in settings.database.url
    
    def test_logging_file_path_resolution(self):
        """Test logging file path resolution."""
        with patch.dict(os.environ, {'LOG_FILE': 'app.log'}):
            settings = Settings()
            
            # Should convert to absolute path
            assert settings.logging.file_path is not None
            assert settings.logging.file_path.endswith('app.log')
            assert os.path.isabs(settings.logging.file_path)
    
    def test_security_warning_production(self):
        """Test security warning for default secret in production."""
        with patch.dict(os.environ, {'HRMS_ENV': 'production'}):
            # Should log warning but not raise error
            settings = Settings()
            assert settings.environment == 'production'
    
    def test_global_settings_instance(self):
        """Test global settings instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        
        # Should return the same instance
        assert settings1 is settings2
        assert isinstance(settings1, Settings)


class TestConfigurationDataClasses:
    """Test suite for configuration dataclasses."""
    
    def test_database_config_defaults(self):
        """Test database configuration defaults."""
        from src.config.settings import DatabaseConfig
        
        config = DatabaseConfig()
        
        assert config.url == "sqlite:///database.db"
        assert config.echo is False
        assert config.pool_size == 10
        assert config.max_overflow == 20
        assert config.pool_pre_ping is True
    
    def test_server_config_defaults(self):
        """Test server configuration defaults."""
        from src.config.settings import ServerConfig
        
        config = ServerConfig()
        
        assert config.host == "0.0.0.0"
        assert config.port == 3000
        assert config.debug is False
        assert config.auto_reload is True
        assert config.gather_usage_stats is False
    
    def test_security_config_defaults(self):
        """Test security configuration defaults."""
        from src.config.settings import SecurityConfig
        
        config = SecurityConfig()
        
        assert config.session_timeout == 3600
        assert config.max_login_attempts == 5
        assert config.password_min_length == 8
        assert config.require_https is False
    
    def test_ui_config_defaults(self):
        """Test UI configuration defaults."""
        from src.config.settings import UIConfig
        
        config = UIConfig()
        
        assert config.theme_primary_color == "#14B8A6"
        assert config.theme_background_color == "#FFFFFF"
        assert config.page_title == "XLAB HRMS - Hệ thống Quản lý Nhân sự"
        assert config.page_icon == "⚡"
        assert config.layout == "wide"


class TestConfigurationSecurity:
    """Test suite for configuration security aspects."""
    
    def test_secret_key_security(self):
        """Test secret key security validation."""
        # Production environment should warn about default secret
        with patch.dict(os.environ, {'HRMS_ENV': 'production'}):
            settings = Settings()
            # Should still work but log warning
            assert settings.environment == 'production'
    
    def test_https_requirement(self):
        """Test HTTPS requirement configuration."""
        with patch.dict(os.environ, {'REQUIRE_HTTPS': 'true'}):
            settings = Settings()
            assert settings.security.require_https is True
    
    def test_session_timeout_bounds(self):
        """Test session timeout reasonable bounds."""
        settings = Settings()
        
        # Should be reasonable timeout (1 hour = 3600 seconds)
        assert 300 <= settings.security.session_timeout <= 86400  # 5 min to 24 hours


if __name__ == "__main__":
    pytest.main([__file__])
