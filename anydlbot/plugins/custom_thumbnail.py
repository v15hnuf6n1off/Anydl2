#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os

from pyrogram import filters

from anydlbot import auth_users, fphoto
from anydlbot.bot import AnyDLBot
from anydlbot.config import Config

# the Strings used for this "thing"
from translation import Translation


@AnyDLBot.on_message(auth_users & fphoto)
async def save_photo(bot, update):
    download_location = os.path.join(Config.WORK_DIR, str(update.from_user.id) + ".jpg")
    await bot.download_media(message=update, file_name=download_location)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.SAVED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id,
    )


@AnyDLBot.on_message(filters.command(["deletethumbnail"]) & auth_users)
async def delete_thumbnail(bot, update):
    download_location = os.path.join(Config.WORK_DIR, str(update.from_user.id))
    try:
        os.remove(download_location + ".jpg")
        # os.remove(download_location + ".json")
    except:
        pass
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id,
    )
