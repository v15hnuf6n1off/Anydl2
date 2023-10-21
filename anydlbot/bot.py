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

# This file was referenced and modified after
# https://github.com/SpEcHiDe/PyroGramBot/blob/master/pyrobot/pyrobot.py
# which is a part of SpEcHiDe/PyroGramBot project released under the "AGPL-3.0 License Agreement".
# All credit goes to its respective owners

import shutil

from pyrogram import Client

from anydlbot import LOGGER
from anydlbot.config import Config


class AnyDLBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()

        plugins = dict(root=f"{name}/plugins")
        super().__init__(
            session_name="anydlbot",           
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            parse_mode="html",
            plugins=plugins,
        )

    async def start(self):
        await super().start()
        bot = await self.get_me()

        LOGGER.info(f"AnyDLBot started on @{bot.username}")

    async def stop(self, *args):
        await super().stop()

        shutil.rmtree(Config.WORK_DIR, ignore_errors=True)
        LOGGER.info("AnyDLBot stopped. Bye.")
