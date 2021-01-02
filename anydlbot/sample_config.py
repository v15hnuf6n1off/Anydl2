import os


class Config:
    LOGGER = True
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 0))
    API_HASH = os.environ.get("API_HASH")
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    # the download location, where the HTTP Server runs
    WORK_DIR = os.environ.get("WORK_DIR", "./DOWNLOADS")
    AUTH_USERS = {os.environ.get("AUTH_USERS", 0)}
    if os.environ.get("AUTH_USERS"):
        AUTH_USERS.update(map(int, os.environ.get("AUTH_USERS").split()))

    # Telegram maximum file upload size
    MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", 50000000))
    TG_MAX_FILE_SIZE = int(os.environ.get("TG_MAX_FILE_SIZE", 2097152000))
    FREE_USER_MAX_FILE_SIZE = int(os.environ.get("FREE_USER_MAX_FILE_SIZE", 50000000))
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 4096))
    PROCESS_MAX_TIMEOUT = int(os.environ.get("PROCESS_MAX_TIMEOUT", 3600))
    # default thumbnail to be used in the videos
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90")
    # proxy for accessing youtube-dl in GeoRestricted Areas
    # Get your own proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = os.environ.get("HTTP_PROXY", None)
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = int(os.environ.get("MAX_MESSAGE_LENGTH", 4096))
    # add config vars for the display progress
    FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "█")
    UN_FINISHED_PROGRESS_STR = os.environ.get("UN_FINISHED_PROGRESS_STR", "░")
