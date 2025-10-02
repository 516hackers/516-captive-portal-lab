import os
from datetime import timedelta

class Config:
    # Basic Flask Config
    SECRET_KEY = os.environ.get('SECRET_KEY', '516-hackers-insecure-key-for-lab')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production (disabled for lab)
    
    # Portal Configuration
    PORTAL_CONFIG = {
        'ssid': '516-Hackers-Lab',
        'welcome_message': '516 Hackers Security Training Portal',
        'redirect_url': 'https://516hackers.org',
        'session_timeout': 3600,
        'max_devices': 10,
        'admin_email': 'admin@516hackers.org'
    }
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    }
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_DEFAULT = "200 per hour"
    
    # Database
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://portal-db:6379/0')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
