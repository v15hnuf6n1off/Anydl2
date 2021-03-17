#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

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
