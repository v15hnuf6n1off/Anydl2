# AnyDLBot - An Open Source ALL-In-One Telegram RoBot
# Copyright (C) 2018-2021 Shrimadhav U K & Authors

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This file was referenced and modified after
# https://github.com/UsergeTeam/Userge-Assistant/blob/master/assistant/config.py
# which is a part of UsergeTeam/Userge-Assistant project released under the "GNU v3.0 License Agreement".
# All credit goes to its respective owners

import os


class Config:
    # Get these two values from my.telegram.org/apps.
    APP_ID = int(os.environ.get("APP_ID", 0))
    API_HASH = os.environ.get("API_HASH")
    # Create a bot using @BotFather, and get the API token.
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    # Directory to handle all downloads
    WORK_DIR = os.environ.get("WORK_DIR", os.path.join(os.getcwd(), "DOWNLOADS"))
    # [Mandatory] The Telegram userid(s) of the separated by a space.
    # Only the users specified here can use this bot.
    USER_IDS = {os.environ.get("USER_IDS", 0)}
    if os.environ.get("USER_IDS"):
        USER_IDS.update(map(int, os.environ.get("USER_IDS").split()))
    USER_IDS = list(USER_IDS)
    # Specify filesize limit here. Currently 2GB(2000*1024*1024)
    TG_MAX_FILE_SIZE = int(os.environ.get("TG_MAX_FILE_SIZE", 2097152000))
    # CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 4096))
    PROCESS_MAX_TIMEOUT = int(os.environ.get("PROCESS_MAX_TIMEOUT", 3600))
    # DEFAULT_THUMBNAIL = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://graph.org/file/03a2199fc52d292cc2422.jpg")
    MAX_MESSAGE_LENGTH = int(os.environ.get("MAX_MESSAGE_LENGTH", 4096))
    # Minimum duration (in seconds)for the video to have for screenshot generation, 15 minutes.
    MIN_DURATION = int(os.environ.get("MIN_DURATION", 900))
    # Specify design for progress block
    FINISHED_PROGRESS_BLOCK = os.environ.get("FINISHED_PROGRESSp_BLOCK", "█")
    UNFINISHED_PROGRESS_BLOCK = os.environ.get("UNFINISHED_PROGRESS_BLOCK", "░")
