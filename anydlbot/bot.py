#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# https://github.com/SpEcHiDe/PyroGramBot/blob/master/pyrobot/pyrobot.py

from pyrogram import Client

from anydlbot import APP_ID, API_HASH, BOT_TOKEN, WORK_DIR, LOGGER


class AnyDLBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()

        plugins = dict(root=f"{name}/plugins")
        super().__init__(
            session_name=":memory:",
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workdir=WORK_DIR,
            parse_mode="html",
            plugins=plugins
        )

    async def start(self):
        await super().start()
        bot = await self.get_me()

        LOGGER.info(f"AnyDLBot started on @{bot.username}")

    async def stop(self, *args):
        await super().stop()
        LOGGER.info("AnyDLBot stopped. Bye.")
