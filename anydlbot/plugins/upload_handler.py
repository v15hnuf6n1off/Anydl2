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

import os
import time
from datetime import datetime
from tempfile import TemporaryDirectory

import magic
from pyrogram.types import InputMediaPhoto

from anydlbot import LOGGER
from anydlbot.config import Config
from anydlbot.helper_funcs.display_progress import humanbytes, progress_for_pyrogram
from anydlbot.helper_funcs.ffmpeg_helper import generate_screenshots
from anydlbot.helper_funcs.metadata import width_and_height, media_duration
from strings import String


async def upload_worker(update, filename, download_directory):
    thumb_image_path = os.path.join(Config.WORK_DIR, str(update.from_user.id) + ".jpg")
    download_directory_dirname = os.path.dirname(download_directory)
    download_directory_contents = os.listdir(download_directory_dirname)
    LOGGER.info(download_directory_contents)
    for download_directory_c in download_directory_contents:
        current_file_name = os.path.join(
            download_directory_dirname, download_directory_c
        )
        file_size = os.stat(current_file_name).st_size

        if file_size > Config.TG_MAX_FILE_SIZE:
            await update.message.edit_caption(
                caption=String.RCHD_TG_API_LIMIT.format(humanbytes(file_size))
            )
            return

        # get the correct width, height, and duration
        # for videos greater than 10MB
        # ref: message from @BotSupport
        width = height = duration = 0
        if os.path.exists(thumb_image_path):
            width, height = width_and_height(thumb_image_path)
        else:
            thumb_image_path = None

        mime_type = magic.from_file(filename=current_file_name, mime=True)
        start_upload = datetime.now()
        c_time = time.time()
        if mime_type.startswith("audio"):
            duration = media_duration(current_file_name)
            await update.message.reply_audio(
                audio=current_file_name,
                caption=filename,
                parse_mode="HTML",
                duration=duration,
                thumb=thumb_image_path,
                progress=progress_for_pyrogram,
                progress_args=(String.UPLOAD_START, update.message, c_time),
            )

        elif mime_type.startswith("video"):
            duration = media_duration(current_file_name)
            await update.message.reply_video(
                video=current_file_name,
                caption=filename,
                parse_mode="HTML",
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                thumb=thumb_image_path,
                progress=progress_for_pyrogram,
                progress_args=(String.UPLOAD_START, update.message, c_time),
            )

        else:
            await update.message.reply_document(
                document=current_file_name,
                thumb=thumb_image_path,
                caption=filename,
                parse_mode="HTML",
                progress=progress_for_pyrogram,
                progress_args=(String.UPLOAD_START, update.message, c_time),
            )

        end_upload = datetime.now()
        time_taken_for_upload = (end_upload - start_upload).seconds
        with TemporaryDirectory(
            prefix="screenshots", dir=download_directory_dirname
        ) as tempdir:
            min_duration = 300
            media_album_p = []
            if mime_type.startswith("video") and duration > min_duration:
                images = generate_screenshots(current_file_name, tempdir, duration, 5)
                LOGGER.info(images)
                i = 0
                caption = f"© @AnyDLBot - Uploaded in {time_taken_for_upload} seconds"
                for image in images:
                    if os.path.exists(image):
                        if i == 0:
                            media_album_p.append(
                                InputMediaPhoto(
                                    media=image, caption=caption, parse_mode="html"
                                )
                            )
                        else:
                            media_album_p.append(InputMediaPhoto(media=image))
                        i += 1
            await update.message.reply_media_group(
                media=media_album_p, disable_notification=True
            )
        #
        return True
