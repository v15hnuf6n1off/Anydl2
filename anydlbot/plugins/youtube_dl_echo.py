#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os
import re

import youtube_dl
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message
from pykeyboard import InlineKeyboard

from anydlbot import LOGGER
from anydlbot.bot import AnyDLBot
from anydlbot.config import Config
from anydlbot.helper_funcs.display_progress import humanbytes
from anydlbot.helper_funcs.extract_link import get_link
from anydlbot.helper_funcs.help_uploadbot import DownLoadFile

# the Strings used for this "thing"
from translation import Translation

regex = re.compile(
    r"https?://(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_+.~#?&/=]*)"
)


@AnyDLBot.on_message(filters.regex(regex) & filters.user(Config.USER_IDS))
async def echo(_, update: Message):
    LOGGER.info(update.from_user)
    url, _, youtube_dl_username, youtube_dl_password = get_link(update)

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
            await update.reply_text(text=str(ytdl_error), quote=True)
            return False

    if info:
        # logger.info(response_json)
        ikeyboard = InlineKeyboard()
        duration = None
        if "duration" in info:
            duration = info["duration"]
        if "formats" in info:
            for formats in info["formats"]:
                format_id = formats.get("format_id")
                format_string = formats.get("format_note")
                if format_string is None:
                    format_string = formats.get("format")
                # @SpEcHiDe/PublicLeech//helper_funcs/youtube_dl_extractor.py#L100
                if "DASH" in format_string.upper():
                    continue
                format_ext = formats.get("ext")
                approx_file_size = ""
                if "filesize" in formats:
                    approx_file_size = humanbytes(formats["filesize"])
                cb_string_video = f"video|{format_id}|{format_ext}"
                cb_string_file = f"file|{format_id}|{format_ext}"
                if format_string and "audio only" not in format_string:
                    ikeyboard.row(
                        InlineKeyboardButton(
                            f"{format_string} Video {format_ext}", cb_string_video
                        ),
                        InlineKeyboardButton(
                            f"Document {approx_file_size}", cb_string_file
                        ),
                    )
                else:
                    # special weird case :\
                    ikeyboard.row(
                        InlineKeyboardButton(
                            f"Video {approx_file_size}", cb_string_video
                        ),
                        InlineKeyboardButton(
                            f"Document {approx_file_size}", cb_string_file
                        ),
                    )
            if duration is not None:
                cb_string_64 = "audio|64|mp3"
                cb_string_128 = "audio|128|mp3"
                cb_string = "audio|320|mp3"
                ikeyboard.row(
                    InlineKeyboardButton("MP3 (64 kbps)", cb_string_64),
                    InlineKeyboardButton("MP3 (128 kbps)", cb_string_128),
                )
                ikeyboard.row(InlineKeyboardButton("MP3 (320 kbps)", cb_string))
        else:
            format_id = info["format_id"]
            format_ext = info["ext"]
            cb_string_file = f"file|{format_id}|{format_ext}"
            cb_string_video = f"video|{format_id}|{format_ext}"
            ikeyboard.row(
                InlineKeyboardButton("Video", cb_string_video),
                InlineKeyboardButton("Document", cb_string_file),
            )
            cb_string_file = f"file={format_id}={format_ext}"
            cb_string_video = f"video={format_id}={format_ext}"
            ikeyboard.row(
                InlineKeyboardButton("video", cb_string_video),
                InlineKeyboardButton("file", cb_string_file),
            )
        # logger.info(reply_markup)
        thumbnail = Config.DEFAULT_THUMBNAIL
        thumbnail_image = Config.DEFAULT_THUMBNAIL
        save_thumbnail = os.path.join(
            Config.WORK_DIR, str(update.from_user.id) + ".jpg"
        )
        if not os.path.isdir(Config.WORK_DIR):
            os.makedirs(Config.WORK_DIR)
        if "thumbnail" in info:
            if info["thumbnail"] is not None:
                thumbnail = info["thumbnail"]
                thumbnail_image = info["thumbnail"]
        if os.path.exists(save_thumbnail):
            thumb_image_path = save_thumbnail
        else:
            thumb_image_path = DownLoadFile(
                thumbnail_image,
                save_thumbnail,
                128,
                None,  # bot,
                Translation.DOWNLOAD_START,
                update.message_id,
                update.chat.id,
            )
        await update.reply_photo(
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
        cb_string_file = "file=LFO=NONE"
        cb_string_video = "video=OFL=ENON"
        ikeyboard.row(
            InlineKeyboardButton("Video", cb_string_video),
            InlineKeyboardButton("Document", cb_string_file),
        )
        await update.reply_photo(
            photo=Config.DEFAULT_THUMBNAIL,
            quote=True,
            caption=Translation.FORMAT_SELECTION.format(""),
            reply_markup=ikeyboard,
            parse_mode="html",
            reply_to_message_id=update.message_id,
        )
