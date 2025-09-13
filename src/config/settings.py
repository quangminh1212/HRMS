#!/usr/bin/env python3
"""
XLAB HRMS Configuration Management

International standards compliant configuration system with:
- Environment-based configuration
- Type safety
- Validation
- Security best practices
- Documentation
"""

import os
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional


# Configure logging for configuration module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DatabaseConfig:
    """Database configuration with type safety."""
    url: str = "sqlite:///database.db"
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20
    pool_pre_ping: bool = True


@dataclass
class ServerConfig:
    """Server configuration for Streamlit application."""
    host: str = "0.0.0.0"
    port: int = 3000
    debug: bool = False
    auto_reload: bool = True
    gather_usage_stats: bool = False


@dataclass
class SecurityConfig:
    """Security configuration with best practices."""
    secret_key: str = "xlab-hrms-secure-key-change-in-production"
    session_timeout: int = 3600  # 1 hour in seconds
    max_login_attempts: int = 5
    password_min_length: int = 8
    require_https: bool = False  # Set to True in production


@dataclass
class LoggingConfig:
    """Logging configuration for the application."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


@dataclass
class UIConfig:
    """UI/UX configuration for consistent theming."""
    theme_primary_color: str = "#14B8A6"  # Teal
    theme_background_color: str = "#FFFFFF"  # White
    theme_secondary_bg_color: str = "#F8FAFC"  # Light gray
    theme_text_color: str = "#0D1421"  # Bunker
    page_title: str = "XLAB HRMS - Hệ thống Quản lý Nhân sự"
    page_icon: str = "⚡"
    layout: str = "wide"


class Settings:
    """
    Main settings class with environment variable support.
    
    Follows international configuration management patterns.
    """
    
    def __init__(self) -> None:
        """Initialize settings with environment variables."""
        self.environment = os.getenv("HRMS_ENV", "development")
        self.base_dir = Path(__file__).parent.parent.parent
        
        # Initialize configuration sections
        self.database = self._load_database_config()
        self.server = self._load_server_config()
        self.security = self._load_security_config()
        self.logging = self._load_logging_config()
        self.ui = self._load_ui_config()
        
        # Validate configuration
        self._validate_config()
        
        logger.info(f"Configuration loaded for environment: {self.environment}")
    
    def _load_database_config(self) -> DatabaseConfig:
        """Load database configuration from environment."""
        db_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
        
        # Ensure SQLite database path is absolute
        if db_url.startswith("sqlite:///") and not db_url.startswith("sqlite:////"):
            db_file = db_url.replace("sqlite:///", "")
            if not os.path.isabs(db_file):
                db_url = f"sqlite:///{self.base_dir / db_file}"
        
        return DatabaseConfig(
            url=db_url,
            echo=os.getenv("DB_ECHO", "false").lower() == "true",
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
            pool_pre_ping=os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"
        )
    
    def _load_server_config(self) -> ServerConfig:
        """Load server configuration from environment."""
        return ServerConfig(
            host=os.getenv("SERVER_HOST", "0.0.0.0"),
            port=int(os.getenv("SERVER_PORT", "3000")),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            auto_reload=os.getenv("AUTO_RELOAD", "true").lower() == "true",
            gather_usage_stats=os.getenv("GATHER_STATS", "false").lower() == "true"
        )
    
    def _load_security_config(self) -> SecurityConfig:
        """Load security configuration from environment."""
        return SecurityConfig(
            secret_key=os.getenv("SECRET_KEY", "xlab-hrms-secure-key-change-in-production"),
            session_timeout=int(os.getenv("SESSION_TIMEOUT", "3600")),
            max_login_attempts=int(os.getenv("MAX_LOGIN_ATTEMPTS", "5")),
            password_min_length=int(os.getenv("PASSWORD_MIN_LENGTH", "8")),
            require_https=os.getenv("REQUIRE_HTTPS", "false").lower() == "true"
        )
    
    def _load_logging_config(self) -> LoggingConfig:
        """Load logging configuration from environment."""
        log_file = os.getenv("LOG_FILE")
        if log_file and not os.path.isabs(log_file):
            log_file = str(self.base_dir / "logs" / log_file)
        
        return LoggingConfig(
            level=os.getenv("LOG_LEVEL", "INFO").upper(),
            format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            file_path=log_file,
            max_file_size=int(os.getenv("LOG_MAX_FILE_SIZE", str(10 * 1024 * 1024))),
            backup_count=int(os.getenv("LOG_BACKUP_COUNT", "5"))
        )
    
    def _load_ui_config(self) -> UIConfig:
        """Load UI configuration from environment."""
        return UIConfig(
            theme_primary_color=os.getenv("THEME_PRIMARY_COLOR", "#14B8A6"),
            theme_background_color=os.getenv("THEME_BG_COLOR", "#FFFFFF"),
            theme_secondary_bg_color=os.getenv("THEME_SECONDARY_BG_COLOR", "#F8FAFC"),
            theme_text_color=os.getenv("THEME_TEXT_COLOR", "#0D1421"),
            page_title=os.getenv("PAGE_TITLE", "XLAB HRMS - Hệ thống Quản lý Nhân sự"),
            page_icon=os.getenv("PAGE_ICON", "⚡"),
            layout=os.getenv("PAGE_LAYOUT", "wide")
        )
    
    def _validate_config(self) -> None:
        """Validate configuration values."""
        # Validate port range
        if not (1024 <= self.server.port <= 65535):
            raise ValueError(f"Invalid port number: {self.server.port}")
        
        # Validate secret key in production
        if self.environment == "production":
            if self.security.secret_key == "xlab-hrms-secure-key-change-in-production":
                logger.warning("Using default secret key in production environment!")
        
        # Validate logging level
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.logging.level not in valid_levels:
            raise ValueError(f"Invalid log level: {self.logging.level}")
        
        logger.info("Configuration validation completed successfully")
    
    def get_streamlit_config(self) -> Dict[str, Any]:
        """
        Get Streamlit-specific configuration dictionary.
        
        Returns:
            Dict[str, Any]: Streamlit configuration options
        """
        return {
            "server.port": self.server.port,
            "server.address": self.server.host,
            "browser.gatherUsageStats": self.server.gather_usage_stats,
            "theme.primaryColor": self.ui.theme_primary_color,
            "theme.backgroundColor": self.ui.theme_background_color,
            "theme.secondaryBackgroundColor": self.ui.theme_secondary_bg_color,
            "theme.textColor": self.ui.theme_text_color,
        }
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get global settings instance.
    
    Returns:
        Settings: Global configuration instance
    """
    return settings
