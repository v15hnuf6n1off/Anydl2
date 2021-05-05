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

from pathlib import Path, PurePath
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from PIL import Image
from pyrogram import filters

from anydlbot import LOGGER
from anydlbot.bot import AnyDLBot
from anydlbot.config import Config
from strings import String


@AnyDLBot.on_message(filters.sticker & filters.user(Config.USER_IDS))
async def sticker_downloader(_, message):
    """Copying @DownloadStickersBot"""
    LOGGER.info(message.from_user)
    sticker = message.sticker
    pack_name = sticker.set_name
    pack_link = f"http://t.me/addstickers/{pack_name}"
    sticker_ext = PurePath(message.sticker.file_name).suffix
    zipfile_name = f"{str(message.from_user.id)}_{pack_name}{sticker_ext}.zip"

    Path(Config.WORK_DIR).mkdir(
        exist_ok=True
    )  # Cause TemporaryDirectory failed to create parent directory
    with TemporaryDirectory(dir=Config.WORK_DIR) as tempdir:
        status = await message.reply_text(
            text=String.DOWNLOAD_START, reply_to_message_id=message.message_id
        )
        try:
            download_to = await message.download(
                file_name=f"{tempdir}/", progress_args=String.DOWNLOAD_START
            )
        except ValueError as e:
            await status.edit_text(text=str(e))
            return False
        await status.edit_text(
            text=String.STICKER_INFO.format(
                sticker.set_name, sticker.emoji, sticker.file_id
            )
        )
        final_location = PurePath(download_to)
        LOGGER.info(final_location)  # /app/DOWNLOADS/<tempdir>/sticker.webp

        zipfile_path = (
            str(final_location.parent) + f"/{zipfile_name}"
        )  # /app/DOWNLOADS/<tempdir>/<zipfile_name>
        with ZipFile(zipfile_path, "w") as stickerZip:
            stickerZip.write(final_location, final_location.name)

        if sticker_ext == ".webp":
            png_location = Path(final_location.with_name(final_location.stem + ".png"))
            LOGGER.info(png_location)  # /app/DOWNLOADS/<tempdir>/sticker.png
            # https://stackoverflow.com/a/21669827/4723940
            Image.open(download_to).convert("RGB").save(png_location, "PNG")

            await status.reply_photo(
                photo=png_location, reply_to_message_id=status.message_id
            )

        await status.reply_document(
            document=zipfile_path,
            caption=pack_link,
            reply_to_message_id=status.message_id,
        )
