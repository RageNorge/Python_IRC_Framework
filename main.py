import socket
import os
config_file_name = "config.py"

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

# Prompts user to set options, write them to file
def create_config():
    # Config steps allow for easy additions later
    config_steps = "5"
    config_file = open(config_file_name, 'w')

    bot_name = input("[1/" + config_steps + "] Name of your bot: ")
    nickserv_password = input("[2/" + config_steps + "] NickServ password: ")
    irc_server = input("[3/" + config_steps + "] IRC server to join: ")
    # All IRC channels start with '#' so it is already added and will be written automatically
    irc_channel = input("[4/" + config_steps + "] IRC channel to join: #")
    join_message = input("[5/" + config_steps + "] Bot's join message (blank for none): ")


    config_file.write("# IRC bot config file\n")
    config_file.write("bot_name=\"" + bot_name + "\"\n")
    config_file.write("nickserv_password=\"" + nickserv_password +"\"\n")
    config_file.write("server=\"" + irc_server + "\"\n")
    config_file.write("channel=\"#" + irc_channel + "\"\n")

    # Join message is optional, so here it is only written to config if it is not blank
    if join_message.strip() is not "":
        config_file.write("join_message=\"" + join_message + "\"\n")

    config_file.close()
    print("Config file " + config_file_name + " was created.")
    print("You may modify this config file manually at any time.")

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

if file_exists(config_file_name):
    # Take the config file name and remove extension then import it
    config_file = __import__(os.path.splitext(config_file_name)[0]) 
    print("Config file \"" + config_file_name + "\" exists.")
    connect()

    while True:
        text = get_text().strip()
        if text != "":
            print(text)

        if "PING" in text:
            ping()

        # 376 signals that the MOTD is over
        if "376" in text:
            identify_name()

        # This waits for a response from nickserv to prevent issues joining +R channels
        if "You are now logged in as " + config_file.bot_name in text:
            join_channel()
            send_join_message()

else:
    print("Config file was not found")

    # Input is lowered and sliced so anything starting with 'y' or 'Y' will work
    if input("Create a new config file? y/n: ").lower()[0:1]  == "y":
        create_config()

