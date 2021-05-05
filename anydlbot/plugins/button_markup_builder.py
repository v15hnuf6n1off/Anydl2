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

import re

import youtube_dl
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton

from anydlbot import LOGGER
from anydlbot.bot import AnyDLBot
from anydlbot.config import Config
from anydlbot.helper_funcs.display_progress import humanbytes
from anydlbot.helper_funcs.extract_link import get_link
from anydlbot.plugins.ytdl_download_handler import yt_extract_info
from strings import String

regex = re.compile(
    r"https?://(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_+.~#?&/=]*)"
)


@AnyDLBot.on_message(filters.regex(regex) & filters.user(Config.USER_IDS))
async def echo(_, message):
    LOGGER.info(message.from_user)
    url, _, youtube_dl_username, youtube_dl_password = get_link(message)

    info_dict = {}
    if youtube_dl_username and youtube_dl_password:
        info_dict.update(
            {
                "username": youtube_dl_username,
                "password": youtube_dl_password,
            }
        )
    if "hotstar" in url:
        info_dict.update(
            {
                "geo_bypass_country": "IN",
            }
        )
    try:
        info = await yt_extract_info(
            video_url=url,
            download=False,
            ytdl_opts=info_dict,
            ie_key=None,
        )
    except youtube_dl.utils.DownloadError as ytdl_error:
        await message.reply_text(text=ytdl_error, quote=True)
        return False

    ikeyboard = InlineKeyboard()
    if info:
        extractor_key = info.get("extractor_key", "Generic")
        duration = info.get("duration", None)
        if "formats" in info:
            for formats in info.get("formats"):
                format_id = formats.get("format_id")
                format_string = formats.get("format_note", None)
                if format_string is None:
                    format_string = formats.get("format")
                # @SpEcHiDe/PublicLeech//helper_funcs/youtube_dl_extractor.py#L100
                if "DASH" in format_string.upper():
                    continue
                format_ext = formats.get("ext")
                av_codec = "empty"
                if formats.get("acodec") == "none" or formats.get("vcodec") == "none":
                    av_codec = "none"
                approx_file_size = (
                    humanbytes(formats.get("filesize"))
                    if formats.get("filesize")
                    else ""
                )
                display_str = (
                    f"{format_string} [{format_ext.upper()}] {approx_file_size}"
                )
                cb_string_video = f"video|{extractor_key}|{format_id}|{av_codec}"
                # GDrive gets special pass, acodec is not listed here, ie acodec=None
                if (
                    extractor_key == "GoogleDrive"
                    and format_id == "source"
                    or extractor_key != "GoogleDrive"
                    and format_string
                    and "audio only" not in format_string
                ):
                    ikeyboard.row(
                        InlineKeyboardButton(display_str, callback_data=cb_string_video)
                    )
                elif extractor_key != "GoogleDrive":
                    # special weird case :\
                    ikeyboard.row(
                        InlineKeyboardButton(
                            f"Video {approx_file_size}", cb_string_video
                        ),
                    )
            if duration:
                ikeyboard.row(
                    InlineKeyboardButton(
                        "MP3 (64 kbps)", callback_data=f"audio|{extractor_key}|64|mp3"
                    ),
                    InlineKeyboardButton(
                        "MP3 (128 kbps)", callback_data=f"audio|{extractor_key}|128|mp3"
                    ),
                )
                ikeyboard.row(
                    InlineKeyboardButton(
                        "MP3 (320 kbps)", callback_data=f"audio|{extractor_key}|320|mp3"
                    )
                )
        elif "entries" in info:
            for entries in info.get("entries"):
                for formats in entries.get("formats"):
                    format_id = formats.get("format_id")
                    format_ext = formats.get("ext")
                    cb_string_file = f"file|{extractor_key}|{format_id}|{format_ext}"
                    ikeyboard.row(
                        InlineKeyboardButton(
                            f"YTDL Generic File [{format_ext.upper()}]",
                            callback_data=cb_string_file,
                        ),
                    )
        else:
            format_id = info.get("format_id")
            format_ext = info.get("ext")
            cb_string_file = f"file={extractor_key}={format_id}={format_ext}"
            ikeyboard.row(
                InlineKeyboardButton(
                    f"File [{format_ext.upper()}]", callback_data=cb_string_file
                ),
            )
    else:
        # fallback for nonnumeric port a.k.a seedbox.io
        cb_string_file = "file=LFO=NONE=NONE"
        ikeyboard.row(
            InlineKeyboardButton("File", callback_data=cb_string_file),
        )

    await message.reply_text(
        text=String.FORMAT_SELECTION.format("")
        + "\n"
        + String.SET_CUSTOM_USERNAME_PASSWORD,
        quote=True,
        reply_markup=ikeyboard,
    )
