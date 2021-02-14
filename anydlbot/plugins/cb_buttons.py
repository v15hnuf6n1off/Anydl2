#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

from pyrogram.types import CallbackQuery

from anydlbot import auth_users
from anydlbot.bot import AnyDLBot
from anydlbot.plugins.dl_button import ddl_call_back
from anydlbot.plugins.youtube_dl_button import youtube_dl_call_back


@AnyDLBot.on_callback_query(auth_users)
async def button(bot, update: CallbackQuery):
    # NOTE: You should always answer,
    # but we want different conditionals to
    # be able to answer to differnetly
    # (and we can only answer once),
    # so we don't always answer here.
    await update.answer()

    cb_data = update.data
    if "|" in cb_data:
        await youtube_dl_call_back(bot, update)
    elif "=" in cb_data:
        await ddl_call_back(bot, update)
