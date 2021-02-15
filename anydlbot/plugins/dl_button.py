#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import asyncio
import os
import time
from datetime import datetime

import aiohttp

from anydlbot import LOGGER
from anydlbot.config import Config
from anydlbot.helper_funcs.display_progress import TimeFormatter, humanbytes
from anydlbot.helper_funcs.extract_link import get_link
from anydlbot.plugins.uploader import upload_worker

# the Strings used for this "thing"
from translation import Translation


async def ddl_call_back(bot, update):
    LOGGER.info(update)
    cb_data = update.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("=")
    thumb_image_path = Config.WORK_DIR + "/" + str(update.from_user.id) + ".jpg"

    (
        youtube_dl_url,
        custom_file_name,
        _,
        _,
    ) = get_link(update.message.reply_to_message)
    if not custom_file_name:
        custom_file_name = os.path.basename(youtube_dl_url)

    description = Translation.CUSTOM_CAPTION_UL_FILE
    start_download = datetime.now()
    await bot.edit_message_text(
        text=Translation.DOWNLOAD_START,
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
    )
    tmp_directory_for_each_user = os.path.join(
        Config.WORK_DIR, str(update.from_user.id)
    )
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = os.path.join(tmp_directory_for_each_user, custom_file_name)

    async with aiohttp.ClientSession() as session:
        c_time = time.time()
        try:
            await download_coroutine(
                bot,
                session,
                youtube_dl_url,
                download_directory,
                update.message.chat.id,
                update.message.message_id,
                c_time,
            )
        except asyncio.TimeoutError:
            await bot.edit_message_text(
                text=Translation.SLOW_URL_DECED,
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
            )
            return False
    if os.path.exists(download_directory):
        end_download = datetime.now()
        time_taken_for_download = (end_download - start_download).seconds
        await bot.edit_message_text(
            text=f"Download took {time_taken_for_download} seconds.\n"
            + Translation.UPLOAD_START,
            chat_id=update.message.chat.id,
            message_id=update.message.message_id,
        )
        try:
            upl = await upload_worker(
                update, "none", tg_send_type, False, download_directory
            )
            LOGGER.info(upl)
        except:
            return False

        try:
            os.remove(download_directory)
            os.remove(thumb_image_path)
        except:
            pass
        await update.message.delete()

    else:
        await bot.edit_message_text(
            text=Translation.NO_VOID_FORMAT_FOUND.format("Incorrect Link"),
            chat_id=update.message.chat.id,
            message_id=update.message.message_id,
            disable_web_page_preview=True,
        )


async def download_coroutine(bot, session, url, file_name, chat_id, message_id, start):
    downloaded = 0
    display_message = ""
    async with session.get(url, timeout=Config.PROCESS_MAX_TIMEOUT) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        await bot.edit_message_text(
            chat_id,
            message_id,
            text="""Initiating Download
URL: {}
File Size: {}""".format(
                url, humanbytes(total_length)
            ),
        )
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(Config.CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += Config.CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    # percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    # elapsed_time = round(diff) * 1000
                    time_to_completion = (
                        round((total_length - downloaded) / speed) * 1000
                    )
                    # estimated_total_time = elapsed_time + time_to_completion
                    try:
                        current_message = """**Download Status**
URL: {}
File Size: {}
Downloaded: {}
ETA: {}

©️ @AnyDLBot""".format(
                            url,
                            humanbytes(total_length),
                            humanbytes(downloaded),
                            TimeFormatter(time_to_completion),
                        )
                        if current_message != display_message:
                            await bot.edit_message_text(
                                chat_id, message_id, text=current_message
                            )
                            display_message = current_message
                    except Exception as e:
                        LOGGER.info(str(e))
                        pass
        return await response.release()
