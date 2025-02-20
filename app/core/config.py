class Settings:
    PROJECT_NAME: str = "User Profile API"
    PROJECT_VERSION: str = "1.0.0"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = 12345678
    MYSQL_SERVER: str = "localhost"
    MYSQL_DB: str = "user_profile_db"
    DATABASE_URL: str = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{MYSQL_DB}"
    UPLOAD_DIR: str = "uploads"

settings = Settings()
