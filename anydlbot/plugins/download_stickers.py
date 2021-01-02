#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os
import time

from PIL import Image
from pyrogram import Client, filters

from anydlbot import AUTH_USERS, WORK_DIR, LOGGER
from anydlbot.helper_funcs.display_progress import progress_for_pyrogram
# the Strings used for this "thing"
from translation import Translation


@Client.on_message(filters.sticker & AUTH_USERS)
async def DownloadStickersBot(_, update):
    if update.sticker.is_animated:
        await update.delete()
        return

    LOGGER.info(update.from_user)
    LOGGER.info(update)
    download_location = os.path.join(
        WORK_DIR,
        str(update.from_user.id) + "_DownloadStickersBot_" +
        str(update.from_user.id) + ".png"
    )
    a = await update.reply_text(
        text=Translation.DOWNLOAD_START,
        reply_to_message_id=update.message_id
    )
    try:
        c_time = time.time()
        the_real_download_location = await update.download(
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.DOWNLOAD_START,
                a,
                c_time
            )
        )
    except ValueError as e:
        await a.edit_text(
            text=str(e)
        )
        return False
    await a.edit_text(
        text=Translation.SAVED_RECVD_DOC_FILE
    )
    # https://stackoverflow.com/a/21669827/4723940
    Image.open(the_real_download_location).convert(
        "RGB"
    ).save(the_real_download_location)
    #
    c_time = time.time()
    await a.reply_document(
        document=the_real_download_location,
        # thumb=thumb_image_path,
        # caption=description,
        # reply_markup=reply_markup,
        # reply_to_message_id=a.message_id,
        progress=progress_for_pyrogram,
        progress_args=(
            Translation.UPLOAD_START,
            a,
            c_time
        )
    )
    await a.reply_photo(
        photo=the_real_download_location,
        # thumb=thumb_image_path,
        # caption=description,
        # reply_markup=reply_markup,
        # reply_to_message_id=a.message_id,
        progress=progress_for_pyrogram,
        progress_args=(
            Translation.UPLOAD_START,
            a,
            c_time
        )
    )
    os.remove(the_real_download_location)
    await a.delete()
