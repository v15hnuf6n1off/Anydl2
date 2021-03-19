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
import re

import youtube_dl
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
from pykeyboard import InlineKeyboard

from anydlbot import LOGGER
from anydlbot.bot import AnyDLBot
from anydlbot.config import Config
from anydlbot.helper_funcs.display_progress import humanbytes
from anydlbot.helper_funcs.extract_link import get_link
from anydlbot.helper_funcs.aiohttp_helper import get_thumbnail

# the Strings used for this "thing"
from translation import Translation

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
    with youtube_dl.YoutubeDL(info_dict) as ytdl:
        try:
            info = ytdl.extract_info(url, download=False)
        except youtube_dl.utils.DownloadError as ytdl_error:
            await message.reply_text(text=str(ytdl_error), quote=True)
            return False

    if info:
        ikeyboard = InlineKeyboard()

        thumb_image = info.get("thumbnail", None)
        thumbnail = thumb_image if thumb_image else Config.DEFAULT_THUMBNAIL

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
                acodec = formats.get("acodec", None)
                approx_file_size = (
                    humanbytes(formats.get("filesize"))
                    if formats.get("filesize")
                    else ""
                )
                special_display_str = (
                    f"{format_string} [{format_ext.upper()}] {approx_file_size}"
                )
                cb_string_video = f"video|{extractor_key}|{format_id}|{acodec}"
                cb_string_document = f"document|{extractor_key}|{format_id}|{acodec}"
                # GDrive gets special pass, acodec is not listed here, ie acodec=None
                if extractor_key == "GoogleDrive":
                    if format_id == "source":
                        ikeyboard.row(
                            InlineKeyboardButton(
                                special_display_str, callback_data=cb_string_video
                            )
                        )
                else:
                    if format_string and "audio only" not in format_string:
                        ikeyboard.row(
                            InlineKeyboardButton(
                                f"{format_string} Video {format_ext}", cb_string_video
                            ),
                            InlineKeyboardButton(
                                f"Document {approx_file_size}", cb_string_document
                            ),
                        )
                    else:
                        # special weird case :\
                        ikeyboard.row(
                            InlineKeyboardButton(
                                f"Video {approx_file_size}", cb_string_video
                            ),
                            InlineKeyboardButton(
                                f"Document {approx_file_size}", cb_string_document
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
        else:
            format_id = info.get("format_id")
            format_ext = info.get("ext")
            cb_string_video = f"video={extractor_key}={format_id}={format_ext}"
            cb_string_document = f"document={extractor_key}={format_id}={format_ext}"
            ikeyboard.row(
                InlineKeyboardButton(f"Video [{format_ext.upper()}]", cb_string_video),
                InlineKeyboardButton(
                    f"Document [{format_ext.upper()}]", cb_string_document
                ),
            )

        save_thumbnail = os.path.join(
            Config.WORK_DIR, str(message.from_user.id) + ".jpg"
        )
        if not os.path.isdir(Config.WORK_DIR):
            os.makedirs(Config.WORK_DIR)

        if os.path.exists(save_thumbnail):
            thumb_image_path = save_thumbnail
        else:
            thumb_image_path = await get_thumbnail(thumbnail, save_thumbnail)
        await message.reply_photo(
            photo=thumb_image_path,
            quote=True,
            caption=Translation.FORMAT_SELECTION.format(thumbnail)
            + "\n"
            + Translation.SET_CUSTOM_USERNAME_PASSWORD,
            reply_markup=ikeyboard,
            parse_mode="html",
        )
    else:
        # fallback for nonnumeric port a.k.a seedbox.io
        ikeyboard = InlineKeyboard()
        cb_string_file = "file=LFO=NONE=NONE"
        cb_string_video = "video=OFL=ENON=NONE"
        ikeyboard.row(
            InlineKeyboardButton("Video", cb_string_video),
            InlineKeyboardButton("Document", cb_string_file),
        )
        await message.reply_photo(
            photo=Config.DEFAULT_THUMBNAIL,
            quote=True,
            caption=Translation.FORMAT_SELECTION.format(""),
            reply_markup=ikeyboard,
            parse_mode="html",
            reply_to_message_id=message.message_id,
        )
