import os
import time
from datetime import datetime

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram.types import InputMediaPhoto

from anydlbot import LOGGER
from anydlbot.config import Config
from anydlbot.helper_funcs.display_progress import humanbytes, progress_for_pyrogram
from anydlbot.helper_funcs.help_Nekmo_ffmpeg import generate_screen_shots

# the Strings used for this "thing"
from translation import Translation


async def upload_worker(update, filename, send_as, generatess, download_directory):
    tmp_directory_for_each_user = os.path.join(
        Config.WORK_DIR, str(update.from_user.id)
    )
    thumb_image_path = os.path.join(Config.WORK_DIR, str(update.from_user.id) + ".jpg")
    download_directory_dirname = os.path.dirname(download_directory)
    download_directory_contents = os.listdir(download_directory_dirname)
    for download_directory_c in download_directory_contents:
        current_file_name = os.path.join(
            download_directory_dirname, download_directory_c
        )
        file_size = os.stat(current_file_name).st_size

        if file_size > Config.TG_MAX_FILE_SIZE:
            await update.message.edit_caption(
                caption=Translation.RCHD_TG_API_LIMIT.format(humanbytes(file_size))
            )
        else:
            if generatess:
                is_w_f = False
                images = await generate_screen_shots(
                    current_file_name, tmp_directory_for_each_user, is_w_f, "", 300, 9
                )
                LOGGER.info(images)
        # get the correct width, height, and duration
        # for videos greater than 10MB
        # ref: message from @BotSupport
        width = 0
        height = 0
        duration = 0
        if send_as != "file":
            metadata = extractMetadata(createParser(current_file_name))
            if metadata is not None:
                if metadata.has("duration"):
                    duration = metadata.get("duration").seconds
        # get the correct width, height, and duration
        # for videos greater than 10MB
        if os.path.exists(thumb_image_path):
            # https://stackoverflow.com/a/21669827/4723940
            Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
            metadata = extractMetadata(createParser(thumb_image_path))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
        else:
            thumb_image_path = None
        start_upload = datetime.now()
        if send_as == "audio":
            await update.message.reply_audio(
                audio=current_file_name,
                caption=os.path.basename(current_file_name),
                parse_mode="HTML",
                duration=duration,
                # performer=response_json["uploader"],
                # title=response_json["title"],
                # reply_markup=reply_markup,
                thumb=thumb_image_path,
                progress=progress_for_pyrogram,
                progress_args=(Translation.UPLOAD_START, update.message, time.time()),
            )

        elif send_as == "file":
            await update.message.reply_document(
                document=current_file_name,
                thumb=thumb_image_path,
                caption=os.path.basename(current_file_name),
                parse_mode="HTML",
                # reply_markup=reply_markup,
                progress=progress_for_pyrogram,
                progress_args=(Translation.UPLOAD_START, update.message, time.time()),
            )

        elif send_as == "video":
            await update.message.reply_video(
                video=current_file_name,
                caption=os.path.basename(current_file_name),
                parse_mode="HTML",
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                # reply_markup=reply_markup,
                thumb=thumb_image_path,
                progress=progress_for_pyrogram,
                progress_args=(Translation.UPLOAD_START, update.message, time.time()),
            )

        else:
            LOGGER.info("Did this happen? :\\")
        end_upload = datetime.now()
        time_taken_for_upload = (end_upload - start_upload).seconds
        media_album_p = []
        if generatess and images:
            i = 0
            caption = f"© @AnyDLBot - Uploaded in {time_taken_for_upload} seconds"
            for image in images:
                if os.path.exists(image):
                    if i == 0:
                        media_album_p.append(
                            InputMediaPhoto(
                                media=image, caption=caption, parse_mode="html"
                            )
                        )
                    else:
                        media_album_p.append(InputMediaPhoto(media=image))
                    i = i + 1
        await update.message.reply_media_group(
            media=media_album_p, disable_notification=True
        )
        #
        return True
