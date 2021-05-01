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

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image


def width_and_height(thumbnail_path):
    metadata = extractMetadata(createParser(thumbnail_path))
    return metadata.get("width"), metadata.get("height")


def media_duration(media_path):
    metadata = extractMetadata(createParser(media_path))
    return metadata.get("duration").seconds


# @SpEcHiDe/PublicLeech/torrent-leecher/tobrot/helper_funcs/upload_to_tg.py#L150-L164
def resize_thumbnail(thumbnail_path):
    width, height = width_and_height(thumbnail_path)
    # resize image
    # ref: https://t.me/PyrogramChat/44663
    # https://stackoverflow.com/a/21669827/4723940
    Image.open(thumbnail_path).convert("RGB").save(thumbnail_path)
    img = Image.open(thumbnail_path)
    # https://stackoverflow.com/a/37631799/4723940
    img.resize((320, height))
    img.save(thumbnail_path, "JPEG")
    # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
