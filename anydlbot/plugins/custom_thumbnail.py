#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os

from pyrogram import Client, filters

from anydlbot import AUTH_USERS, WORK_DIR, LOGGER
# the Strings used for this "thing"
from translation import Translation


@Client.on_message(filters.photo & AUTH_USERS)
async def save_photo(bot, update):
    download_location = os.path.join(
        WORK_DIR,
        str(update.from_user.id) + ".jpg"
    )
    await bot.download_media(
        message=update,
        file_name=download_location
    )
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.SAVED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["deletethumbnail"]) & AUTH_USERS)
async def delete_thumbnail(bot, update):
    download_location = os.path.join(
        WORK_DIR,
        str(update.from_user.id)
    )
    try:
        os.remove(download_location + ".jpg")
        # os.remove(download_location + ".json")
    except:
        pass
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )
