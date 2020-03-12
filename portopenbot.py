import json
import telebot
import sys
import os
import subprocess

commands_list = {
    "/uptime": "uptime",
    "/df": "df -ht ext4 -t vfat",
    "/ps": "ps ao %mem,%cpu,cmd,pid --sort=-%mem | head",
    "/free": "free -hm",
    "/sensors": "sensors",
    "/ip": "ip -4 -br address show enp2s0f0",
}

def config_file_path():
    """Construct path to config file"""
    script_dir = os.path.dirname(__file__)
    config_file = script_dir + "/bot_config.json"
    return config_file


def new_config(token=None, user_id=None):
    """Creating new config file in interactive mode"""

    if token and user_id:
        return
    if not token:
        token = input("\nСкопируйте token бота:")
    if not user_id:
        user_id = input("\nСкопируйте user_id получателя сообщений:")

    config_file = config_file_path()
    with open(config_file, "w") as f:
        json.dump(dict(token=token, user_id=user_id), f)
        print("Configuration saved.")


def load_config():
    """Loading token and user_id from json-file"""
    config_file = config_file_path()

    if not os.path.exists(config_file):
        new_config()

    with open(config_file, "r") as f:
        try:
            config = json.load(f)
            print(config.get("user_id"))
            user_id = config.get("user_id")
            token = config.get("token")
        except FileNotFoundError:
            print("Config file not found. Creating new config")
            new_config()
        except json.decoder.JSONDecodeError:
            print("Incorrect config format.")
            new_config()

    token = config.get("token")
    user_id = config.get("user_id")
    # new_config(token=token, user_id=user_id)
    return token, user_id


def command_run(command):
    """Run command in shell and catch output"""
    print("==>", command)
    run = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    print(">", run.stdout.decode())
    return run.stdout.decode()


def ssh_port_change(bot, user_id):
    """Call external bash script to on/of sshd. Check ssh_onoff.sh for additional info"""
    command = "sudo " + os.path.dirname(__file__) + "/ssh_onoff.sh"

    bot.send_message(user_id, command_run(command))


def main():
    token, user_id = load_config()
    bot = telebot.TeleBot(token)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        print(message.text)
        command = commands_list.get(message.text)

        if command:
            bot.send_message(user_id, command_run(command))
        elif message.text == "/ssh":
            ssh_port_change(bot, user_id)
        else:
            bot.send_message(user_id, "Unknown command")

    bot.polling(none_stop=True, interval=2)


if __name__ == "__main__":

    if sys.platform != 'linux':
        exit("Скрипт предназначен для запуска на машине с linux")
    main()
