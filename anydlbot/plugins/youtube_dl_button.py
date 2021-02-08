#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os
import shutil
import time
from datetime import datetime

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from pyrogram.types import InputMediaPhoto
import youtube_dl

from anydlbot import LOGGER
from anydlbot.config import Config
from anydlbot.helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from anydlbot.helper_funcs.help_Nekmo_ffmpeg import generate_screen_shots
from anydlbot.helper_funcs.extract_link import get_link
# the Strings used for this "thing"
from translation import Translation


async def youtube_dl_call_back(_, update):
    cb_data = update.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("|")
    thumb_image_path = os.path.join(Config.WORK_DIR, str(update.from_user.id) + ".jpg")

    youtube_dl_url, \
        custom_file_name, \
        youtube_dl_username, \
        youtube_dl_password = get_link(
            update.message.reply_to_message
        )
    if not custom_file_name:
        custom_file_name = "%(title)s.%(ext)s"
    await update.message.edit_caption(
        caption=Translation.DOWNLOAD_START
    )
    # description = Translation.CUSTOM_CAPTION_UL_FILE
    tmp_directory_for_each_user = os.path.join(
        Config.WORK_DIR,
        str(update.from_user.id)
    )
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = os.path.join(
        tmp_directory_for_each_user,
        custom_file_name
    )
    ytdl_opts = {
        "outtmpl": download_directory,
        "ignoreerrors": True,
        "nooverwrites": True,
        "continuedl": True,
        "noplaylist": True,
        "max_filesize": Config.TG_MAX_FILE_SIZE,
    }
    if youtube_dl_username and youtube_dl_password:
        ytdl_opts.update({
            "username": youtube_dl_username,
            "password": youtube_dl_password,
        })
    if "hotstar" in youtube_dl_url:
        ytdl_opts.update({
            "geo_bypass_country": "IN",
        })
    if tg_send_type == "audio":
        ytdl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": youtube_dl_ext,
                "preferredquality": youtube_dl_format
            }, {
                "key": "FFmpegMetadata"
            }],
        })
    elif tg_send_type == "video":
        minus_f_format = youtube_dl_format
        if "youtu" in youtube_dl_url:
            minus_f_format = f"{youtube_dl_format}+bestaudio"
        ytdl_opts.update({
            "format": minus_f_format,
            "postprocessors": [{
                "key": "FFmpegMetadata"
            }],
        })

    start = datetime.now()
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        info = ytdl.extract_info(youtube_dl_url, download=False)
        title = info.get("title", None)
        yt_task = ytdl.download([youtube_dl_url])

    if yt_task == 0:
        end_one = datetime.now()
        time_taken_for_download = (end_one - start).seconds
        download_directory_dirname = os.path.dirname(download_directory)
        download_directory_contents = os.listdir(download_directory_dirname)
        for download_directory_c in download_directory_contents:
            current_file_name = os.path.join(
                download_directory_dirname,
                download_directory_c
            )
            file_size = os.stat(current_file_name).st_size

            if file_size > Config.TG_MAX_FILE_SIZE:
                await update.message.edit_caption(
                    caption=Translation.RCHD_TG_API_LIMIT.format(
                        time_taken_for_download,
                        humanbytes(file_size)
                    )
                )

            else:
                is_w_f = False
                images = await generate_screen_shots(
                    current_file_name,
                    tmp_directory_for_each_user,
                    is_w_f,
                    "",
                    300,
                    9
                )
                LOGGER.info(images)
                await update.message.edit_caption(
                    caption=f"Download took {time_taken_for_download} seconds.\n" +
                            Translation.UPLOAD_START
                )
                # get the correct width, height, and duration
                # for videos greater than 10MB
                # ref: message from @BotSupport
                width = 0
                height = 0
                duration = 0
                if tg_send_type != "file":
                    metadata = extractMetadata(createParser(current_file_name))
                    if metadata is not None:
                        if metadata.has("duration"):
                            duration = metadata.get('duration').seconds
                # get the correct width, height, and duration
                # for videos greater than 10MB
                if os.path.exists(thumb_image_path):
                    # https://stackoverflow.com/a/21669827/4723940
                    Image.open(thumb_image_path).convert(
                        "RGB"
                    ).save(thumb_image_path)
                    metadata = extractMetadata(createParser(thumb_image_path))
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    if tg_send_type == "vm":
                        height = width
                else:
                    thumb_image_path = None
                start_time = time.time()
                # try to upload file
                if tg_send_type == "audio":
                    await update.message.reply_audio(
                        audio=current_file_name,
                        caption=title,
                        parse_mode="HTML",
                        duration=duration,
                        # performer=response_json["uploader"],
                        # title=response_json["title"],
                        # reply_markup=reply_markup,
                        thumb=thumb_image_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                elif tg_send_type == "file":
                    await update.message.reply_document(
                        document=current_file_name,
                        thumb=thumb_image_path,
                        caption=title,
                        parse_mode="HTML",
                        # reply_markup=reply_markup,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                elif tg_send_type == "video":
                    await update.message.reply_video(
                        video=current_file_name,
                        caption=title,
                        parse_mode="HTML",
                        duration=duration,
                        width=width,
                        height=height,
                        supports_streaming=True,
                        # reply_markup=reply_markup,
                        thumb=thumb_image_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                else:
                    LOGGER.info("Did this happen? :\\")
                end_two = datetime.now()
                time_taken_for_upload = (end_two - end_one).seconds
                #
                media_album_p = []
                if images is not None:
                    i = 0
                    caption = f"© @AnyDLBot - Uploaded in {time_taken_for_upload} seconds"
                    for image in images:
                        if os.path.exists(image):
                            if i == 0:
                                media_album_p.append(
                                    InputMediaPhoto(
                                        media=image,
                                        caption=caption,
                                        parse_mode="html"
                                    )
                                )
                            else:
                                media_album_p.append(
                                    InputMediaPhoto(
                                        media=image
                                    )
                                )
                            i = i + 1
                await update.message.reply_media_group(
                    media=media_album_p,
                    disable_notification=True
                )
            #
            shutil.rmtree(
                tmp_directory_for_each_user,
                ignore_errors=True
            )
            LOGGER.info("Cleared temporary folder")
            os.remove(thumb_image_path)

            await update.message.delete()
