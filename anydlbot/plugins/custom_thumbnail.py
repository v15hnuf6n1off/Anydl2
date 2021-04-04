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

from anydlbot.bot import AnyDLBot
from anydlbot.config import Config
from strings import String


@AnyDLBot.on_message(filters.photo & filters.user(Config.USER_IDS))
async def save_photo(bot, update):
    download_location = os.path.join(Config.WORK_DIR, str(update.from_user.id) + ".jpg")
    await bot.download_media(message=update, file_name=download_location)
    await bot.send_message(
        chat_id=update.chat.id,
        text=String.SAVED_CUSTOM_THUMBNAIL,
        reply_to_message_id=update.message_id,
    )


@AnyDLBot.on_message(filters.command("deletethumbnail") & filters.user(Config.USER_IDS))
async def delete_thumbnail(bot, update):
    download_location = os.path.join(Config.WORK_DIR, str(update.from_user.id))
    try:
        os.remove(download_location + ".jpg")
        # os.remove(download_location + ".json")
    except:
        pass
    await bot.send_message(
        chat_id=update.chat.id,
        text=String.DELETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id,
    )
