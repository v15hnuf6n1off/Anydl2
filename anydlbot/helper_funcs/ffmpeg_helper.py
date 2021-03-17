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

import ffmpeg
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from anydlbot import LOGGER


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
        return output_file if output_file else None


def generate_screenshots(input_file, output_dir, min_duration, no_of_photos):
    metadata = extractMetadata(createParser(input_file))
    duration = 0
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds
    if duration > min_duration:
        images = []
        ttl_step = duration // no_of_photos
        current_ttl = ttl_step
        for _ in range(0, no_of_photos):
            ss_img = screencapture(input_file, output_dir, current_ttl)
            current_ttl = current_ttl + ttl_step
            if ss_img is not None:
                images.append(ss_img)
        return images
