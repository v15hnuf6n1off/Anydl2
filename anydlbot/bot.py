#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# https://github.com/SpEcHiDe/PyroGramBot/blob/master/pyrobot/pyrobot.py

import shutil
from pyrogram import Client
from anydlbot import LOGGER
from anydlbot.config import Config


class AnyDLBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()

        plugins = dict(root=f"{name}/plugins")
        super().__init__(
            session_name=":memory:",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            parse_mode="html",
            plugins=plugins
        )

    async def start(self):
        await super().start()
        bot = await self.get_me()

        LOGGER.info(f"AnyDLBot started on @{bot.username}")

    async def stop(self, *args):
        await super().stop()

        shutil.rmtree(Config.WORK_DIR, ignore_errors=True)
        LOGGER.info("AnyDLBot stopped. Bye.")
