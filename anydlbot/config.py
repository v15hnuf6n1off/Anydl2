import os


class Config:
    APP_ID = int(os.environ.get("APP_ID", 0))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    WORK_DIR = os.environ.get("WORK_DIR", "./DOWNLOADS")
    AUTH_USERS = {os.environ.get("AUTH_USERS", [12345])}
    if os.environ.get("AUTH_USERS"):
        AUTH_USERS.update(map(int, os.environ.get("AUTH_USERS").split()))
    TG_MAX_FILE_SIZE = int(os.environ.get("TG_MAX_FILE_SIZE", 2097152000))
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 4096))
    PROCESS_MAX_TIMEOUT = int(os.environ.get("PROCESS_MAX_TIMEOUT", 3600))
    DEF_THUMB_NAIL_VID_S = os.environ.get(
        "DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90"
    )
    MAX_MESSAGE_LENGTH = int(os.environ.get("MAX_MESSAGE_LENGTH", 4096))
    FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "█")
    UN_FINISHED_PROGRESS_STR = os.environ.get("UN_FINISHED_PROGRESS_STR", "░")
