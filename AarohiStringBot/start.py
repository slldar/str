from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""- مرحباً عزيزي {msg.from_user.mention}.
     
     - انا بوت لأستخراج جلسات التليثون و البايروجرام .

- المطور  : [SLiDaR](tg://user?id={OWNER_ID}) .""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=". اضغط لأستخراج الجلسه .", callback_data="generate")
                ],
                [
                    InlineKeyboardButton(". 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 .", url="https://t.me/c8_8x"),
                    InlineKeyboardButton(". 𝖣𝖾𝖵𝖾𝖫𝗈𝖯𝖾𝖱 .", user_id=OWNER_ID)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
