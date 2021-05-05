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
import functools
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from tempfile import mkdtemp

import youtube_dl

from anydlbot import LOGGER
from anydlbot.config import Config
from anydlbot.helper_funcs.extract_link import get_link
from anydlbot.plugins.upload_handler import upload_worker
from strings import String


# https://stackoverflow.com/a/64506715
def run_in_executor(_func):
    @functools.wraps(_func)
    async def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        func = functools.partial(_func, *args, **kwargs)
        return await loop.run_in_executor(executor=ThreadPoolExecutor(), func=func)

    return wrapped


@run_in_executor
def yt_extract_info(video_url, download, ytdl_opts, ie_key):
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        info = ytdl.extract_info(video_url, download=download, ie_key=ie_key)
    return info


async def youtube_dl_call_back(_, update):
    cb_data = update.data
    LOGGER.info(cb_data)
    # youtube_dl extractors
    send_as, extractor_key, format_id, av_codec = cb_data.split("|")

    (
        youtube_dl_url,
        custom_file_name,
        youtube_dl_username,
        youtube_dl_password,
    ) = get_link(update.message.reply_to_message)
    if not custom_file_name:
        custom_file_name = "%(title)s.%(ext)s"
    await update.message.edit_text(text=String.DOWNLOAD_START)
    # description = Translation.CUSTOM_CAPTION_UL_FILE
    tmp_directory_for_each_user = os.path.join(
        Config.WORK_DIR, str(update.from_user.id)
    )
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = os.path.join(
        mkdtemp(dir=tmp_directory_for_each_user), custom_file_name
    )
    ytdl_opts = {
        "outtmpl": download_directory,
        "ignoreerrors": True,
        "nooverwrites": True,
        "continuedl": True,
        "noplaylist": True,
        "restrictfilenames": True,
        "max_filesize": Config.TG_MAX_FILE_SIZE,
    }
    if youtube_dl_username and youtube_dl_password:
        ytdl_opts.update(
            {
                "username": youtube_dl_username,
                "password": youtube_dl_password,
            }
        )
    if extractor_key == "HotStar":
        ytdl_opts.update(
            {
                "geo_bypass_country": "IN",
            }
        )
    if send_as == "audio":
        ytdl_opts.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": av_codec,
                        "preferredquality": format_id,
                    },
                    {"key": "FFmpegMetadata"},
                ],
            }
        )
    elif send_as == "video":
        final_format = format_id
        if extractor_key == "Youtube" and av_codec == "none":
            final_format = f"{format_id}+bestaudio"
        ytdl_opts.update(
            {
                "format": final_format,
                "postprocessors": [{"key": "FFmpegMetadata"}],
            }
        )
    elif send_as == "file":
        ytdl_opts.update(
            {
                "format": format_id,
            }
        )

    start_download = datetime.now()
    try:
        info = await yt_extract_info(
            video_url=youtube_dl_url,
            download=True,
            ytdl_opts=ytdl_opts,
            ie_key=extractor_key,
        )
    except youtube_dl.utils.DownloadError as ytdl_error:
        await update.message.edit_text(text=ytdl_error)
        return False

    if info:
        end_download = datetime.now()
        time_taken_for_download = (end_download - start_download).seconds
        await update.message.edit_text(
            text=f"Download took {time_taken_for_download} seconds.\n"
            + String.UPLOAD_START
        )
        upl = await upload_worker(
            update, info.get("title", ""), info.get("thumbnail"), download_directory
        )
        LOGGER.info(upl)
        shutil.rmtree(download_directory, ignore_errors=True)
        LOGGER.info("Cleared temporary folder")

        await update.message.delete()
