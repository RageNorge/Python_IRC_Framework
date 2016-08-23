import socket
import os
import config_handler
config_file_name = "config.py"
modules_folder_name = "modules"

# Use IPv4 and TCP/IP
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Checks to see if a file exists
def file_exists(file_name):
    try:
        f = open(file_name, "r")
        f.close()
        return True
    except:
        return False

def send2irc(irc_cmd, msg):
    irc.send((irc_cmd + " " + msg + "\n").encode())

def connect():
    print("Connecting to \"" + config_file.server + "\".")
    # Connect to server
    irc.connect((config_file.server, 6667))
    # Authenticate user
    send2irc("USER", (config_file.bot_name + " ") * 3 + ":This is a bot.")
    send2irc("NICK", config_file.bot_name)

def join_channel():
    send2irc("JOIN", config_file.channel)

def send_join_message():
    send2irc("PRIVMSG", config_file.channel + " " +  config_file.join_message)

def identify_name():
    send2irc("PRIVMSG", "NickServ :IDENTIFY " + config_file.nickserv_password)

def get_text():
    text = irc.recv(2040)
    # Get text then convert it from bytestring and remove the newlines
    stripped_text = text.decode()
    return stripped_text

def ping():
    send2irc("PONG", text.split()[1] + "\r")

def get_sender_name():
    return get_text().rsplit("!", 1)[0]

if file_exists(config_file_name):
    # Take the config file name and remove extension then import it
    config_file = __import__(os.path.splitext(config_file_name)[0])
    print("Config file \"" + config_file_name + "\" exists.")
    connect()

    while True:
        text = get_text().strip()
        # Remove unicode characters that don't print properly
        text = text.replace("\x02", "").replace("\x1F", "")
        if text != "":
            print(text)

        if "PING" in text:
            ping()

        # 376 signals that the MOTD is over
        elif "376" in text:
            identify_name()

        # This waits for a response from nickserv to prevent issues joining +R channels
        elif "You are now logged in as " + config_file.bot_name in text:
            join_channel()
            send_join_message()

else:
    print("Config file was not found")

    # Input is lowered and sliced so anything starting with 'y' or 'Y' will work
    if input("Create a new config file? y/n: ").lower()[0:1]  == "y":
        config_handler.create_config(config_file_name)
