from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from pyrogram1 import Client as Client1
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram1.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "**- اختار يقلبي عايز تطلع جلسة اي :**"
buttons_ques = [
    [
        InlineKeyboardButton(". بايروجرام v1 .", callback_data="pyrogram1"),
        InlineKeyboardButton(". بايروجرام v2 .", callback_data="pyrogram"),
    ],
    [
        InlineKeyboardButton(". تليثون .", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton(". بايروجرام بوت .", callback_data="pyrogram_bot"),
        InlineKeyboardButton(". تليثون بوت .", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text=". اضغط لأستخراج الجلسات .", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["استخراج"], prefixes=["/", ""]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    if telethon:
        ty = ". تليثون"
    else:
        ty = ". بايروجرام"
        if not old_pyro:
            ty += " v2 ."
    if is_bot:
        ty += " بوت ."
    await msg.reply(f". انتظر قليلاً **{ty}** تحت أمرك .")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "- من فضلك ارسل لي الايبي ايدي  . \n\n - لو هما مش معاك اعمل /skip .", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("-**الايبي ايدي** يحب ان يكون صحيحاً ، ابدء في انشاء جلستك مره اخري .", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "- **ارسل **الايبي هاش .", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = ".- من فضلك ارسل **رقمك** مع رمز الدوله مثل : +20110000000"
    else:
        t = "- من فضلك ارسل **توكن بوتك** مثل : `543216789:slidarelbasha3laibasha`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("- انتظر جاري ارسال الكود علي الرقم المحدد .")
    else:
        await msg.reply("- تسجيل الدخول عبر توكن البوت .")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        await msg.reply("- الايبي ايدي و الايبي هاش** لن يتطابقو مع نظام تطبيقات التليجرام** . \n\n - من فضلك البدء في انشاء الجلسه مره اخري للبدء اضغط /start .", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        await msg.reply("- **رقمك** مش مستخدم تليجرام . \n\n - من فضلك البدء في انشاء الجلسه مره اخري للبدء اضغط /start .", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "- من فضلك ارسلي الكود التي وصلك علي الرقم المحدد مثل - 1 2 3 4 5 - \n\n سيب بين كل رقمين مسافه .", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("- انت اتاخرت في ارسال الكود . \n\ny - دوس /start وابدء في انشاء الجلسه من جديد .", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
            await msg.reply("- من فضلك ارسل /start واعمل الجلسه من جديد .", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
            await msg.reply("- من فضلك ارسل /start واعمل الجلسه من جديد .", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
            try:
                two_step_msg = await bot.ask(user_id, "- ارسل تحقق حسابك .", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("- انت اتأخرت في ارسال التحقق . \n\n- ارسل /start وانشاء الجلسه مره اخري .", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
                await two_step_msg.reply("< 333.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"- تم استخراج الجلسه . \n\n`{string_session}` \n\n - مطور البوت @Q_z_T . \n - لا تعطيها لأحد ."
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "- بص في الرسائل المحفوظه هتلاقي الجلسه . \n\n - ملحوظه متديش الجلسه لحد عشان ممكن يخش حسابك من خلالها . ".format(". تليثون ." if telethon else ". بايروجرام ."))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**» ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀɪɴɢ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴩʀᴏᴄᴇss !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
      await msg.reply("**» sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇsᴛᴀʀᴛᴇᴅ ᴛʜɪs ʙᴏᴛ ғᴏʀ ʏᴏᴜ !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):   Bot Commands
        await msg.reply("**» ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀɪɴɢ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴩʀᴏᴄᴇss !**", quote=True)
        return True
    else:
        return False
