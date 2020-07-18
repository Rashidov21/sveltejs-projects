import telebot
import os
from .models import *

#myBookStore_bot
token ='1325857591:AAH4WZLVviq_omfSXNjxcYsQuzya0ivfBEI'
bot = telebot.TeleBot(token)
my_id = 891196310

def send_add_list_product(delivery_id):
	delivery = AddProductArchive.objects.get(id=delivery_id)
	post = "<b>{0} dan qabul qilingan tovarlar ro'yxati</b>\n<b>Sana:{1}-{2} {3}</b>".format(delivery.provider.name,delivery.day,delivery.month,delivery.year)
	pa =  os.getcwd()
	path = "{0}/{1}".format(pa,delivery.pdf.url)
	file = open(path,'rb')
	bot.send_document(my_id,file,caption=post,parse_mode="HTML")
	return 'ok' 