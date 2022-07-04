import os
import telebot
from flask import Flask, request
import config
import bot

APP_URL = f"https://investbot-webhook.herokuapp.com/{config.TOKEN}"
bot = telebot.TeleBot(config.TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=["start"])
def start(message):
	bot.reply_to(message, "Hi, " + message.from_user.first_name)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo(message):
	bot.reply_to(message, message.text)

@server.route('/' + config.TOKEN, method=['POST'])
def get_message():
	json_string = request.get_data().decode('utf-8')
	update = telebot.types.Update.de_json(json_string)
	bot.process_new_updates([update])
	return '!', 200

@server.route('/')
def webhook():
	bot.remote_webhook()
	bot.set_webhook(url=APP_URL)
	return '!', 200

if __name__ == "__main__":
	server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))