"""Settings for the application"""

from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    ENVIRONMENT_VARIABLES_FILE: str = "backend/.env"
    FILE_ID_BITS: int = 128
    FILE_NAME_PREFIX: str = "/tmp/audio"
    NORMALIZE_DB: float = -20.0
    SUPPORTED_AUDIO_FORMATS: list[str] = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]
    MIN_AUDIO_LENGTH_SECONDS: int = 20
    MAX_AUDIO_MB: int = 25

    AUDIO_REMOVE_SILENCE_ST_WIN: float = 0.040
    AUDIO_REMOVE_SILENCE_ST_STEP: float = 0.040
    AUDIO_REMOVE_SILENCE_SMOOTH_WINDOW: float = 3.0
    AUDIO_REMOVE_SILENCE_WEIGHT: float = 0.3
    AUDIO_REMOVE_SILENCE_PLOT: bool = False

    EMOTIONS_MODEL: str = "j-hartmann/emotion-english-distilroberta-base"
    EMOTIONS_EMBEDDINGS_CHUNKS: int = 512
    EMOTIONS_EMBEDDINGS_MAX_LENGTH: int = 512

    SUMMARIZATION_MODEL: str = "gpt-4o-mini"
    SUMMARIZATION_MODEL_TEMP: float = 0.0

    WHISPER_MODEL: str = "whisper-large-v2"

settings = Settings()
