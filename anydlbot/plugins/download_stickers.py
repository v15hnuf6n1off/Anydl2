#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os
import time

from pyrogram import filters
from PIL import Image

from anydlbot.bot import AnyDLBot
from anydlbot.config import Config
from anydlbot.helper_funcs.display_progress import progress_for_pyrogram

# the Strings used for this "thing"
from translation import Translation


@AnyDLBot.on_message(filters.sticker & filters.user(Config.USER_IDS))
async def DownloadStickersBot(_, update):
    if update.sticker.is_animated:
        await update.delete()
        return

    download_location = os.path.join(
        Config.WORK_DIR,
        str(update.from_user.id)
        + "_DownloadStickersBot_"
        + str(update.from_user.id)
        + ".png",
    )
    a = await update.reply_text(
        text=Translation.DOWNLOAD_START, reply_to_message_id=update.message_id
    )
    try:
        c_time = time.time()
        the_real_download_location = await update.download(
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(Translation.DOWNLOAD_START, a, c_time),
        )
    except ValueError as e:
        await a.edit_text(text=str(e))
        return False
    await a.edit_text(text=Translation.SAVED_RECVD_DOC_FILE)
    # https://stackoverflow.com/a/21669827/4723940
    Image.open(the_real_download_location).convert("RGB").save(
        the_real_download_location
    )
    #
    c_time = time.time()
    await a.reply_document(
        document=the_real_download_location,
        # thumb=thumb_image_path,
        # caption=description,
        # reply_markup=reply_markup,
        # reply_to_message_id=a.message_id,
        progress=progress_for_pyrogram,
        progress_args=(Translation.UPLOAD_START, a, c_time),
    )
    await a.reply_photo(
        photo=the_real_download_location,
        # thumb=thumb_image_path,
        # caption=description,
        # reply_markup=reply_markup,
        # reply_to_message_id=a.message_id,
        progress=progress_for_pyrogram,
        progress_args=(Translation.UPLOAD_START, a, c_time),
    )
    os.remove(the_real_download_location)
    await a.delete()
