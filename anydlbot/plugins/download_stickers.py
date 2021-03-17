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
