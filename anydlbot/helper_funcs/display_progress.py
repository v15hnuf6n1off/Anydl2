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

import math
import time

from anydlbot.config import Config


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        elapsed_time = round(diff)
        if elapsed_time == 0:
            return
        speed = current / elapsed_time
        time_to_completion = round((total - current) / speed)

        estimated_total_time = time_formatter(time_to_completion)

        progress = "[{}{}]\n".format(
            "".join(
                Config.FINISHED_PROGRESS_BLOCK
                for _ in range(math.floor(percentage / 5))
            ),
            "".join(
                Config.UNFINISHED_PROGRESS_BLOCK
                for _ in range(20 - math.floor(percentage / 5))
            ),
        )


        tmp = progress + "Uploading {} of {} at {}/s, ETA: {}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != "" else "0 seconds",
        )
        try:
            await message.edit_text(f"{ud_type}\n {tmp}")
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/43690506
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if size < 1024.0 or unit == "PiB":
            break
        size /= 1024.0
    return f"{size:.2f} {unit}"


def time_formatter(seconds: int) -> str:
    # https://github.com/SpEcHiDe/PublicLeech/blob/master/tobrot/helper_funcs/display_progress.py
    result = ""
    v_m = 0
    remainder = seconds
    r_ange_s = {"days": (24 * 60 * 60), "hours": (60 * 60), "minutes": 60, "seconds": 1}
    for age, divisor in r_ange_s.items():
        v_m, remainder = divmod(remainder, divisor)
        v_m = int(v_m)
        if v_m != 0:
            result += f" {v_m} {age} "
    return result
