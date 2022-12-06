import os
import logging
import random
import asyncio
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, CUSTOM_FILE_CAPTION
from utils import get_size, is_subscribed
import re

logger = logging.getLogger(__name__)


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):    
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('➕ 𝐀𝐃𝐃 𝐌𝐄 𝐓𝐎 𝐘𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏 ➕', url=f'http://t.me/{client.username}?startgroup=true')
        ], [
            InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄𝐒', url='https://t.me/cinemapranthangroup'),
            InlineKeyboardButton('𝐒𝐄𝐑𝐈𝐄𝐒 ⭕️', url='https://t.me/cinemapranthangroup_s')
        ], [
            InlineKeyboardButton('⭕️ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋', url='https://t.me/TinsonTs'),
            InlineKeyboardButton('𝐆𝐑𝐎𝐔𝐏 ⭕️', url='https://t.me/cinemapranthangroup')
        ], [
            InlineKeyboardButton('⭕️ 𝐇𝐄𝐋𝐏', callback_data='help'),
            InlineKeyboardButton('𝐀𝐁𝐎𝐔𝐓 ⭕️', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, client.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [[InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link )]]                
        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)               
                btn.append([InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton(" 🔄 Try Again", url=f"https://t.me/{client.username}?start={message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text="👇 JOIN MY UPDATES CHANNEL AND CLICK 🔄 𝐓𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 TO GET MOVIE 👇 മൂവി ഫയൽ ലഭിക്കാൻ എന്റെ അപ്‌ഡേറ്റ് ചാനലിൽ ചേർന്ന് ശേഷം 🔄 𝐓𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 അമർത്തുക 👇",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
            )
        return    
    data = message.command[1]
    pre, file_id = data.split('_', 1)   
    files_ = await get_file_details(file_id)
    if not files_:            
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    try:
        f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size)        
    except:
        f_caption=f"{title}"
    try:
        await client.send_cached_media(chat_id=message.from_user.id, file_id=file_id, caption=f_caption)
    except Exception as e:
        await client.send_cached_media(chat_id=message.from_user.id, text=f"{e}")       


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                await msg.edit('File not found in database')



@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer('°°°°°')
    await message.message.edit('Succesfully Deleted All The Indexed Files.')

