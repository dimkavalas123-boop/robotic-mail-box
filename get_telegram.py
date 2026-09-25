import telebot
import json
import datetime
import os
import queue

TOKEN = 'SAMPLE'
bot = telebot.TeleBot(TOKEN)

msg_queue = queue.Queue()

JSON_PATH = "texts/delivered.json"

def get_delivered_data():
    with open(JSON_PATH, "r") as f:
        delivered_data = json.load(f)

    return delivered_data

def save_data(delivered_data):
    with open(JSON_PATH, "w") as f:
        json.dump(delivered_data, f, indent=4)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    now = str(datetime.datetime.now())
    new_entry = {"Time": now, "isText": True, "ImagePath": None, "Content": message.text}

    delivered_data = get_delivered_data()
    delivered_data.append(new_entry)
    save_data(delivered_data)

    msg_queue.put("NEW_MSG")
    print("Added to delivered!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    now = str(datetime.datetime.now())    
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    os.makedirs("photos", exist_ok=True)
    photo_path = f"photos/{len(os.listdir('photos'))}.jpg"
    with open(photo_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    new_entry = {"Time": now, "isText": False, "ImagePath": photo_path, "Content": None}
    delivered_data = get_delivered_data()
    delivered_data.append(new_entry)
    save_data(delivered_data)

    msg_queue.put("NEW_MSG")
    print("Added photo to delivered!")    

def run_bot():
    bot.polling(none_stop=True, timeout=10)
