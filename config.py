# config.py

class Config:
    UPLOAD_FOLDER = 'uploads'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Add other configuration classes for different environments if needed