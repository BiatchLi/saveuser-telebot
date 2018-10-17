import telebot
import time
from db_helper import DBHelper
import test 

bot_token = ''

bot = telebot.TeleBot(token=bot_token)

superadmins = [655045110]
db = DBHelper()
# global vars
limit = 100

#-------------------------------------------------privatechats only for admin ------------------


@bot.message_handler(commands=['start'])
def send_welcome(message):
	if message.chat.type == "private" and message.from_user.id in superadmins:
		bot.send_message(
			message.chat.id, 'use /listcommands to see what can i do or send username to save in db only (100) users at a time ')

	elif message.chat.type == "private":
		text = "You have no access to me GET OUT"
		bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['listcommands'])
def handle_text(message):
	if message.chat.type == "private" and message.from_user.id in superadmins:
		text = """ /start - start the privatechat with bot
				   /total - total users in db 
				   /totalcontacted - show total contacted users
				   /totalnotcontacted - show total users not contacted yet
				   /showlimit
				   /setlimit     --- be careful higher limit might result in slower performance and server load
				   note to brodcast message run the script explicitly  
					 """
		bot.send_message(message.chat.id, text)
	elif message.chat.type == "private":
		text = "You have no access to me GET OUT"
		bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['total'])
def send_welcome(message):
	if message.chat.type == "private" and message.from_user.id in superadmins:
		total = db.total()
		text = ' there are '+str(total)+' total users in db '
		bot.send_message(message.chat.id,text)

	elif message.chat.type == "private":
		text = "You have no access to me GET OUT"
		bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['totalcontacted'])
def send_welcome(message):
	if message.chat.type == "private" and message.from_user.id in superadmins:
		total = db.total('contacted')
		text = ' there are '+str(total)+' total contacted users in db '
		bot.send_message(message.chat.id,text)

	elif message.chat.type == "private":
		text = "You have no access to me GET OUT"
		bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['totalnotcontacted'])
def send_welcome(message):
	if message.chat.type == "private" and message.from_user.id in superadmins:
		total = db.total('notcontacted')
		text = ' there are '+str(total)+' total users that have not been yet contacted in db '
		bot.send_message(message.chat.id,text)

	elif message.chat.type == "private":
		text = "You have no access to me GET OUT"
		bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['showlimit'])
def send_welcome(message):
	if message.chat.type == "private" and message.from_user.id in superadmins:
		global limit
		text = ' the current limit for snipped user and contacted user is %s \n'%limit
		text += ' however you can set it according to your preferences using /setlimit  '
		bot.send_message(
			message.chat.id, text )

	elif message.chat.type == "private":
		text = "You have no access to me GET OUT"
		bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['setlimit'])
def send_welcome(message):
	if message.chat.type == "private" and message.from_user.id in superadmins:
		text = 'send the number you want the limit to be and please be careful higher limit might result in slower performance and server load'
		msg = bot.send_message(message.chat.id, text )
		bot.register_next_step_handler(msg,set_limit)

	elif message.chat.type == "private":
		text = "You have no access to me GET OUT"
		bot.send_message(message.chat.id, text)

# ============================================ end ===============================================

@bot.message_handler(content_types=['text'])
def handle_text(message):
	if message.chat.type == "private" and message.from_user.id in superadmins:
		users = message.text.split('\n')
		ignored = []
		text = '  '
		count = 0
		global limit
		client.start()
		if len(users) > limit:
			ignored = users[100:]
			users = users[:100]
			text += ' number of users limit exceeded therefor only first '+str(limit)+' will be considered rest will be ignored \n'
		for user in users:
			try:
				temp = user.replace(" ",'-')
				temp = temp.split('-')
				if len(temp)>1:
					# print(temp, 'hence passed')
					bot.send_message(message.chat.id,'wrong format')
					break
				if not user.lower().startswith('@'):
					user = '@'+user
				# if db.checkifexist(user) is not None:
				if db.checkifexist(user) == None:
					db.add_tlgrm_user(0,user)
					count +=1
			except Exception as e:
				print(e)

		text +=' total '+str(count)+' users added out of '+str(len(users))
		bot.send_message(message.chat.id,text)

	elif message.from_user.id not in superadmins:
		bot.send_message(message.chat.id, ' dont spam me its of no use ')

while True:
	try:
		bot.polling()
	except Exception as e:
		time.sleep(15)
