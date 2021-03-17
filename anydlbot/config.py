import os


class Config:
    APP_ID = int(os.environ.get("APP_ID", 0))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    WORK_DIR = os.environ.get("WORK_DIR", "./DOWNLOADS/")

    USER_IDS = {os.environ.get("USER_IDS", 0)}
    if os.environ.get("USER_IDS"):
        USER_IDS.update(map(int, os.environ.get("USER_IDS").split()))
    USER_IDS = list(USER_IDS)

    TG_MAX_FILE_SIZE = int(os.environ.get("TG_MAX_FILE_SIZE", 2097152000))
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 4096))
    PROCESS_MAX_TIMEOUT = int(os.environ.get("PROCESS_MAX_TIMEOUT", 3600))
    DEFAULT_THUMBNAIL = os.environ.get(
        "DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90"
    )
    MAX_MESSAGE_LENGTH = int(os.environ.get("MAX_MESSAGE_LENGTH", 4096))

    FINISHED_PROGRESS_BLOCK = os.environ.get("FINISHED_PROGRESS_BLOCK", "█")
    UNFINISHED_PROGRESS_BLOCK = os.environ.get("UNFINISHED_PROGRESS_BLOCK", "░")
