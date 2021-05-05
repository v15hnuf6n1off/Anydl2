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

import asyncio
import os
import time

# from datetime import datetime
from tempfile import TemporaryDirectory

import magic
from pyrogram.errors import FloodWait

from anydlbot import LOGGER
from anydlbot.config import Config
from anydlbot.helper_funcs.aiohttp_helper import get_thumbnail
from anydlbot.helper_funcs.display_progress import humanbytes, progress_for_pyrogram
from anydlbot.helper_funcs.ffmpeg_helper import generate_screenshots, screencapture
from anydlbot.helper_funcs.metadata import media_duration, width_and_height
from strings import String


async def upload_worker(update, filename, thumbnail, download_directory):
    download_directory_dirname = os.path.dirname(download_directory)
    download_directory_contents = os.listdir(download_directory_dirname)
    LOGGER.info(download_directory_contents)
    for download_directory_c in download_directory_contents:
        current_file_name = os.path.join(
            download_directory_dirname, download_directory_c
        )
        file_size = os.stat(current_file_name).st_size

        if file_size > Config.TG_MAX_FILE_SIZE:
            await update.message.edit_text(
                text=String.RCHD_TG_API_LIMIT.format(humanbytes(file_size))
            )
            return

        custom_thumb_path = os.path.join(
            Config.WORK_DIR, str(update.from_user.id) + ".jpg"
        )
        temp_thumb_dir = os.path.join(download_directory_dirname, "thumbnail.jpg")
        if os.path.isfile(custom_thumb_path):
            LOGGER.info("Custom thumbnail found. Using this now")
            thumb = custom_thumb_path
        else:
            thumb = (
                await get_thumbnail(thumbnail, temp_thumb_dir) if thumbnail else None
            )

        mime_type = magic.from_file(filename=current_file_name, mime=True)
        # start_upload = datetime.now()
        c_time = time.time()
        width = height = duration = 0
        if mime_type.startswith("audio"):
            duration = media_duration(current_file_name)
            await update.message.reply_audio(
                audio=current_file_name,
                caption=filename,
                parse_mode="HTML",
                duration=duration,
                thumb=thumb,
                progress=progress_for_pyrogram,
                progress_args=(String.UPLOAD_START, update.message, c_time),
            )

        elif mime_type.startswith("video"):
            duration = media_duration(current_file_name)
            if thumb is None:
                thumb = screencapture(
                    current_file_name, download_directory_dirname, duration // 2
                )
                LOGGER.info("Generating thumbnail of the video.")
            if os.path.isfile(thumb):
                width, height = width_and_height(thumb)
            await update.message.reply_video(
                video=current_file_name,
                caption=filename,
                parse_mode="HTML",
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                thumb=thumb,
                progress=progress_for_pyrogram,
                progress_args=(String.UPLOAD_START, update.message, c_time),
            )

        else:
            await update.message.reply_document(
                document=current_file_name,
                thumb=thumb,
                caption=filename,
                parse_mode="HTML",
                progress=progress_for_pyrogram,
                progress_args=(String.UPLOAD_START, update.message, c_time),
            )

        # end_upload = datetime.now()
        # time_taken_for_upload = (end_upload - start_upload).seconds
        with TemporaryDirectory(
            prefix="screenshots", dir=download_directory_dirname
        ) as tempdir:
            if mime_type.startswith("video") and duration > Config.MIN_DURATION:
                media_album_p = generate_screenshots(
                    current_file_name, tempdir, duration, 5
                )
                # LOGGER.info(media_album_p)
                try:
                    await update.message.reply_media_group(
                        media=media_album_p, disable_notification=True
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.x)
        #
        return True
