# Prompts user to set options, write them to file
def create_config(config_file_name):
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
