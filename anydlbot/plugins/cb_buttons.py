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

from pyrogram.types import CallbackQuery

from anydlbot.bot import AnyDLBot
from anydlbot.config import Config
from anydlbot.plugins.dl_button import ddl_call_back
from anydlbot.plugins.youtube_dl_button import youtube_dl_call_back


@AnyDLBot.on_callback_query()
async def button(anydlbot, update: CallbackQuery):
    if update.from_user.id not in Config.USER_IDS:
        return
    # NOTE: You should always answer,
    # but we want different conditionals to
    # be able to answer to differnetly
    # (and we can only answer once),
    # so we don't always answer here.
    await update.answer()

    cb_data = update.data
    if "|" in cb_data:
        await youtube_dl_call_back(anydlbot, update)
    elif "=" in cb_data:
        await ddl_call_back(anydlbot, update)
