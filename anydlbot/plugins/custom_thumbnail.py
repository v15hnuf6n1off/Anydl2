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

from pyrogram import filters

from anydlbot import LOGGER
from anydlbot.bot import AnyDLBot
from anydlbot.config import Config
from anydlbot.helper_funcs.metadata import resize_thumbnail
from strings import String


@AnyDLBot.on_message(filters.photo & filters.user(Config.USER_IDS))
async def save_photo(_, message):
    custom_thumb_path = os.path.join(
        Config.WORK_DIR, str(message.from_user.id) + ".jpg"
    )
    await message.download(file_name=custom_thumb_path)
    if os.path.isfile(custom_thumb_path):
        LOGGER.info("Custom thumbnail saved.")
        resize_thumbnail(custom_thumb_path)
        await message.reply_text(
            text=String.SAVED_CUSTOM_THUMBNAIL,
        )
    else:
        await message.reply_text(
            text=String.FAILED_SAVE_CUSTOM_THUMBNAIL,
        )


@AnyDLBot.on_message(filters.command("deletethumbnail") & filters.user(Config.USER_IDS))
async def delete_thumbnail(_, message):
    custom_thumb_path = os.path.join(
        Config.WORK_DIR, str(message.from_user.id) + ".jpg"
    )
    if os.path.isfile(custom_thumb_path):
        os.remove(custom_thumb_path)
        LOGGER.info("Custom thumbnail removed.")
        await message.reply_text(
            text=String.DELETED_CUSTOM_THUMB_NAIL,
        )
    else:
        await message.reply_text(
            text=String.FAILED_DELETE_CUSTOM_THUMB_NAIL,
        )
