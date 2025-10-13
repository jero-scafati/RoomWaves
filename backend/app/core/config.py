from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Roomwaves"
    APP_DESCRIPTION: str = "Roomwaves is a web application for room acoustics analysis."
    APP_VERSION: str = "1.0.0"
    
    # CORS settings
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "https://roomwaves.vercel.app"
    ]

    # S3/R2 settings
    R2_ENDPOINT_URL: str
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str
    R2_ACCOUNT_ID: str
    
    # File settings
    MAX_FILE_SIZE_MB: int = 25
    ALLOWED_MIME_TYPES: list[str] = [
        "audio/mpeg", "audio/wav", "audio/flac", "audio/aac",
        "audio/ogg", "audio/x-m4a", "audio/mp4"
    ]

    @property
    def MAX_FILE_SIZE_BYTES(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    class Config:
        env_file = ".env"

settings = Settings()
