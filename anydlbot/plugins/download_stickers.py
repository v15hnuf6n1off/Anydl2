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
from random import randint
from zipfile import ZipFile

from pyrogram import filters
from PIL import Image

from anydlbot.bot import AnyDLBot
from anydlbot.config import Config

# the Strings used for this "thing"
from translation import Translation


@AnyDLBot.on_message(filters.sticker & filters.user(Config.USER_IDS))
async def sticker_downloader(_, message):
    """Copying @DownloadStickersBot"""
    sticker = message.sticker
    pack_name = sticker.set_name
    pack_link = f"http://t.me/addstickers/{pack_name}"
    sticker_ext = os.path.splitext(message.sticker.file_name)[1]
    zipfile_name = f"{str(message.from_user.id)}_{pack_name}{sticker_ext}.zip"
    zipfile_path = os.path.join(Config.WORK_DIR, zipfile_name)
    temp_basename = randint(10000, 99999)

    path_to_download = os.path.join(Config.WORK_DIR, str(temp_basename) + sticker_ext)
    if not os.path.exists(Config.WORK_DIR):
        os.makedirs(Config.WORK_DIR)

    status = await message.reply_text(
        text=Translation.DOWNLOAD_START, reply_to_message_id=message.message_id
    )
    try:
        download_location = await message.download(
            file_name=path_to_download, progress_args=Translation.DOWNLOAD_START
        )
    except ValueError as e:
        await status.edit_text(text=str(e))
        return False
    await status.edit_text(
        text=Translation.STICKER_INFO.format(
            sticker.set_name, sticker.emoji, sticker.file_id
        )
    )

    with ZipFile(zipfile_path, "w") as stickerZip:
        stickerZip.write(download_location, os.path.basename(path_to_download))

    if sticker_ext == ".webp":
        file_path, ext = os.path.splitext(download_location)
        png_location = os.path.join(file_path + ".png")
        # https://stackoverflow.com/a/21669827/4723940
        Image.open(download_location).convert("RGB").save(png_location, "PNG")

        await status.reply_photo(
            photo=png_location, reply_to_message_id=status.message_id
        )
        os.remove(png_location)

    await status.reply_document(
        document=zipfile_path, caption=pack_link, reply_to_message_id=status.message_id
    )

    # Cleanup
    os.remove(download_location)
    os.remove(zipfile_path)
