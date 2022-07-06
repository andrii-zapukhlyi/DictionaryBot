import telebot, random, pymongo
from pymongo import MongoClient
#CHANGE ON YOUR MONGODB CLUSTER
cluster = pymongo.MongoClient("link mongodb cluster")
#DATABASE NAME MUST BE 'telegramBot' in your cluster settings!
db = cluster["telegramBot"]
#COLLECTION NAME MUST BE 'dictionaryBot' in your cluster settings!
collection = db["dictionaryBot"]

#CHANGE ON YOUR TELEGRAM BOT ID
bot = telebot.TeleBot('telegramBot Id')

try:
	result = collection.delete_many({"English":"test"})
except: 
	pass

# Variables
complete = 0
eng = []
ukr = []
identifiers = []
rand = random.randint(0,0)

# Keyboard
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('/add')

# Starting bot
@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Bot is ready. Type /add to add new words.')

# Adding words
@bot.message_handler(commands=['add'])
def add_words(message):
	global complete
	eng.clear()
	ukr.clear()
	bot.send_message(message.chat.id, 'Enter the words.')
	complete = 0

# Quiz
@bot.message_handler(content_types=['text'])
def send_text(message):
	global complete
	global rand
	try:
		if complete == 0:
			string = message.text
			array = list(string.split("; "))
			array2 = array.copy()
			array.pop(1)
			array2.pop(0)
			str = ""
			str2 = ""
			for i in array:
				str += i
			for i in array2:
				str2 += i
			eng = list(str.split(", "))
			ukr = list(str2.split(", "))
			engLengh = len(eng)
			ukrLengh = len(ukr)
			if engLengh != ukrLengh:
				bot.send_message(message.chat.id, 'Something went wrong. Type /add to add new words.')
			else:
				for i in range(engLengh):
					obj = {"English": f"{eng[i]}", "Ukrainian": f"{ukr[i]}"}
					collection.insert_one(obj)
				results = collection.find({})
				identifiers.clear()
				for result in results:
					identifiers.append(result["_id"])
				id = identifiers[rand]
				results = collection.find({"_id": id})
				for result in results:
					bot.send_message(message.chat.id, f"{result['English']}?", reply_markup=keyboard1)
				complete = 1
		else:
			id = identifiers[rand]
			results = collection.find({"_id": id})
			for result in results:
				bot.send_message(message.chat.id, f"{result['Ukrainian']}.")
			count = rand
			int = collection.count_documents({})
			i = int - 1
			rand = random.randint(0,i)
			id = identifiers[rand]
			results = collection.find({"_id": id})
			for result in results:
				bot.send_message(message.chat.id, f"{result['English']}?")
	except:
		bot.send_message(message.chat.id, 'Something went wrong. Type /add to add new words.')

bot.polling()
