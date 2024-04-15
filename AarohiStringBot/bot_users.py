from pyrogram.types import Message
from pyrogram import Client, filters

from config import OWNER_ID
from AarohiStringBot.db.users import add_served_user, get_served_users


@Client.on_message(filters.private & ~filters.service, group=1)
async def users_sql(_, msg: Message):
    await add_served_user(msg.from_user.id)


@Client.on_message(filters.user(OWNER_ID) & filters.command(["الاحصائيات"], prefixes=["/", ""]))
async def _stats(_, msg: Message):
    users = len(await get_served_users())
    await msg.reply_text(f"𓏺 𝖼𝖴𝗋𝗋𝖤𝗇𝖳 𝗌𝖳𝖺𝖳𝗌 𝖮𝖥 𝗌𝖳𝖱𝗂𝗇𝖦 𝖦𝖾𝖭 𝖡𝗈𝖳 :\n\n {users}  𝖴𝗌𝖤𝖱𝗌 .", quote=True)
