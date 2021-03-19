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

import time

import aiohttp

from anydlbot import LOGGER
from anydlbot.config import Config
from anydlbot.helper_funcs.display_progress import humanbytes, time_formatter


async def direct_downloader(bot, url, file_name, chat_id, message_id, start):
    async with aiohttp.ClientSession() as session:
        display_message = ""
        async with session.get(url, timeout=Config.PROCESS_MAX_TIMEOUT) as response:
            total_length = int(response.headers["Content-Length"])
            content_type = response.headers["Content-Type"]
            if "text" in content_type and total_length < 500:
                return await response.release()
            await bot.edit_message_text(
                chat_id,
                message_id,
                text=f"Initiating Download \nURL: {url} \nFile Size: {humanbytes(total_length)}",
            )
            with open(file_name, "wb") as f_handle:
                downloaded = 0
                while True:
                    chunk = await response.content.read(Config.CHUNK_SIZE)
                    if not chunk:
                        break
                    f_handle.write(chunk)
                    downloaded += Config.CHUNK_SIZE
                    now = time.time()
                    diff = now - start
                    if round(diff % 5.00) == 0 or downloaded == total_length:
                        elapsed_time = round(diff)
                        if elapsed_time == 0:
                            return
                        speed = downloaded / elapsed_time
                        time_to_completion = (
                            round((total_length - downloaded) / speed) * 1000
                        )
                        try:
                            current_message = f"URL: {url}\n"
                            current_message += (
                                f"Downloaded {humanbytes(downloaded)} of "
                                f"{humanbytes(total_length)} at {humanbytes(speed)}\n"
                                f"ETA: {time_formatter(time_to_completion)}\n"
                            )
                            if current_message != display_message:
                                await bot.edit_message_text(
                                    chat_id, message_id, text=current_message
                                )
                                display_message = current_message
                        except Exception as e:
                            LOGGER.info(str(e))
            return await response.release()
