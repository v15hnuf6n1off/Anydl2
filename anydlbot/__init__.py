#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os

from pyrogram import filters

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# the secret configuration specific things
if bool(os.environ.get("ENV", False)):
    from anydlbot.sample_config import Config
else:
    from anydlbot.config import Config


# TODO: is there a better way?
LOGGER = logging.getLogger(__name__)
BOT_TOKEN = Config.BOT_TOKEN
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
AUTH_USERS = filters.user(list(Config.AUTH_USERS))
WORK_DIR = Config.WORK_DIR
# create download directory, if not exist
if not os.path.isdir(WORK_DIR):
    os.makedirs(WORK_DIR)
MAX_FILE_SIZE = Config.MAX_FILE_SIZE
TG_MAX_FILE_SIZE = Config.TG_MAX_FILE_SIZE
CHUNK_SIZE = Config.CHUNK_SIZE
DEF_THUMB_NAIL_VID_S = Config.DEF_THUMB_NAIL_VID_S
MAX_MESSAGE_LENGTH = Config.MAX_MESSAGE_LENGTH
PROCESS_MAX_TIMEOUT = Config.PROCESS_MAX_TIMEOUT
HTTP_PROXY = Config.HTTP_PROXY
FINISHED_PROGRESS_STR = Config.FINISHED_PROGRESS_STR
UN_FINISHED_PROGRESS_STR = Config.UN_FINISHED_PROGRESS_STR
