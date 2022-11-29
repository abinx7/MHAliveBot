import os
import time
import string
import random
import asyncio
import aiofiles
import datetime
import aiofiles.os
from info import ADMINS
from traceback import format_exc
from pyrogram import Client, filters
from database.users_chats_db import db
from utils import broadcast_messages, temp
from pyrogram.errors import InputUserDeactivated, FloodWait, UserIsBlocked, PeerIdInvalid


@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.private)
async def send_broadcast(bot: Client, update):    
    all_users = await db.get_all_users()
    broadcast_msg = update.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not temp.broadcast_ids.get(broadcast_id):
            break
    out = await update.reply_text(text="**𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃 𝙸𝙽𝙸𝚃𝙸𝙰𝚃𝙴𝙳..📯**\n𝚈𝙾𝚄 𝚆𝙸𝙻𝙻 𝙱𝙴 𝙽𝙾𝚃𝙸𝙵𝙸𝙴𝙳 𝚆𝙸𝚃𝙷 𝙻𝙾𝙶 𝙵𝙸𝙻𝙴 𝚆𝙷𝙴𝙽 𝙰𝙻𝙻 𝚃𝙷𝙴 𝚄𝚂𝙴𝚁𝚂 𝙰𝚁𝙴 𝙽𝙾𝚃𝙸𝙵𝙸𝙴𝙳 🔉")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    temp.broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)            
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            await asyncio.sleep(2)
            if not done % 20:
                await out.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {failed}")   

            if temp.broadcast_ids.get(broadcast_id) is None:
                break
            else:
                temp.broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
                        
    if temp.broadcast_ids.get(broadcast_id):
        temp.broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    await asyncio.sleep(1)    
    await out.delete()
    if failed == 0:
        await update.reply_text(text=f"""**🚀 𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃 𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴𝙳 𝙸𝙽** - `{completed_in}`\n\n𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂 {total_users}.\n𝚃𝙾𝚃𝙰𝙻 𝙳𝙾𝙽𝙴 {done}, {success} 𝚂𝚄𝙲𝙲𝙴𝚂𝚂 & {failed} 𝙵𝙰𝙸𝙻𝙴𝙳""", quote=True)        
    else:
        await update.reply_document(document='broadcast.txt', caption=f"""** 🚀 𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃 𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴𝙳 𝙸𝙽**- `{completed_in}`\n\n𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂 {total_users}.\n𝚃𝙾𝚃𝙰𝙻 𝙳𝙾𝙽𝙴 {done}, {success} 𝚂𝚄𝙲𝙲𝙴𝚂𝚂 & {failed} 𝙵𝙰𝙸𝙻𝙴𝙳""", quote=True)
    await aiofiles.os.remove('broadcast.txt')



async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {format_exc()}\n"



"""

from pyrogram import Client, filters
import datetime
import time
from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages
import asyncio
        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
# https://t.me/GetTGLink/4178
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")

"""
