import main

# Sends message to chat
def send_message(message):
    main.send2irc("PRIVMSG", main.config_file.channel + " " + message)

# Sends a /me action
def send_action(action):
    main.send2irc("PRIVMSG", "\x01ACTION " + action + "\x01")

def get_text():
    main.get_text()

def get_sender_name():
    return main.get_text()[1:].rsplit('!', 1)[0]
