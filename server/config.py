import os


class Settings:
    host: str = os.environ.get("HOST", "0.0.0.0")
    port: int = int(os.environ.get("PORT", "8000"))
    reload: bool = bool(os.environ.get("RELOAD", ""))

    api_key: str = os.environ.get("THIRD_PARTY_API_KEY", "")


def get_settings() -> Settings:
    return Settings()

