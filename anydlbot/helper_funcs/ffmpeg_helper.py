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
from datetime import timedelta

import ffmpeg
from pyrogram.types import InputMediaPhoto

from anydlbot import LOGGER
from strings import String


# https://github.com/kkroening/ffmpeg-python/blob/master/examples/get_video_thumbnail.py
def screencapture(input_file, output_dir, seek_time):
    # https://stackoverflow.com/a/13891070/4723940
    output_file = output_dir + "/" + str(time.time()) + ".jpg"
    try:
        (
            ffmpeg.input(input_file, ss=seek_time)
            .output(output_file, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        LOGGER.info(e.stderr.decode())
    finally:
        return output_file or None


def generate_screenshots(input_file, output_dir, duration, no_of_photos):
    images = []
    ttl_step = duration // no_of_photos
    current_ttl = ttl_step
    for _ in range(no_of_photos):
        ss_img = screencapture(input_file, output_dir, current_ttl)
        if ss_img is not None:
            # Caption showing frame time taken from
            # @odysseusmax/animated-lamp/bot/processes/screenshot.py#L143
            images.append(
                InputMediaPhoto(
                    media=ss_img,
                    caption=String.SCREENSHOT_TAKEN.format(
                        timedelta(seconds=current_ttl)
                    ),
                )
            )
        current_ttl = current_ttl + ttl_step
    return images
