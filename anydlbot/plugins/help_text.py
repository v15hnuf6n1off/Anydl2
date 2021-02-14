#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

from pyrogram import filters

from anydlbot.bot import AnyDLBot

# the Strings used for this "thing"
from translation import Translation


@AnyDLBot.on_message(filters.command(["help", "about"]))
async def help_user(bot, update):
    # LOGGER.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id,
    )


@AnyDLBot.on_message(filters.command(["start"]))
async def start(bot, update):
    # LOGGER.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT,
        reply_to_message_id=update.message_id,
    )
