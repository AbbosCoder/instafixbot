import telebot
from telebot.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from admin import is_admin,reklama,admin_panel,markup,button_yordam
import time
# Bot tokeni bilan botni yaratish
bot = telebot.TeleBot("6336857872:AAEhuNLbwdvjA43QdWyzj4b2mrlOsVpq_PU")

#admin habari
def admin_xabari(message):
    chat_id = message.chat.id 
    msg = bot.send_message(chat_id, "Xabar yuboring:")
    bot.register_next_step_handler(msg, lambda m: xabarlar(m, chat_id))

def xabarlar(message, chat_id):
    caption=message.text
    xabar=ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    text=KeyboardButton("Xabarlarni yuborish")
    media=KeyboardButton("Rasm yoki video qo'shish")
    exit=KeyboardButton("Bekor qilish")
    xabar.add(text,media,exit)      
    msg = bot.send_message(chat_id, "Rasm yoki video yuborasizmi yoki shunday jo'natilsinmi(xabar uchun)?",reply_markup=xabar)
    bot.register_next_step_handler(msg, lambda m: tanlash(m, chat_id, caption))
def tanlash(message,chat_id,caption):
    qaror = message.text
    if qaror=="Xabarlarni yuborish":
        with open('users.txt', 'r') as file:
            users = file.readlines()
            for user in users:
                user_id = user.strip()
                try:
                    bot.send_message(user_id, caption)
                except telebot.apihelper.ApiTelegramException as e:
                    if "bot was blocked by the user" in str(e):
                        print(f"User {user_id} botni bloklagan")
                    else:
                        print(f"Xatolik yuz berdi: {str(e)}")
        bot.send_message(chat_id,f"Admin menyusi:",reply_markup=admin_panel())            
    elif qaror=="Rasm yoki video qo'shish":
        msg=bot.send_message(chat_id,"Unda menga rasm yoki video xabar jo'nating!")
        bot.register_next_step_handler(msg,lambda  m: save_media( m,chat_id,caption))
    elif qaror=='Bekor qilish':
        bot.send_message(chat_id,"Bekor qilindi!\nAdmin menyusi:",reply_markup=admin_panel())
    else:
        bot.reply_to(message,"Nimadir xato ketdi.\nQaytadan urining!")
        admin_xabari(message)    
def get_user_count(file_name):
    try:
        with open(file_name, 'r') as file:
            user_count = len(file.readlines())
            return user_count
    except FileNotFoundError:
        return "Fayl topilmadi."

# Fayl nomini o'rnating
file_name = "users.txt"

@bot.message_handler(content_types=['photo', 'video'])
def save_media(message,chat_id, caption):
 # Rasmni yoki videoni saqlash
    if message.content_type == 'photo' and is_admin(chat_id):
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)
        # Rasmni admin_xabar papkasiga saqlash
        nomii=file_id[15:22]
        with open(f'admin_xabar/{nomii}.jpg', 'wb') as f:
            f.write(file)
            bot.send_message(chat_id, "Rasm va xabar muvaffaqiyatli saqlandi!")
        time.sleep(3)
           
        with open('users.txt', 'r') as file:
            users = file.readlines()
            for user in users:
                user_id = user.strip()
                try:
                    rasm=open(f'admin_xabar/{nomii}.jpg',"rb")
                    bot.send_photo(user_id,photo=rasm,caption=f"{caption}")
                except telebot.apihelper.ApiTelegramException as e:
                    if "bot was blocked by the user" in str(e):
                        print(f"User {user_id} botni bloklagan")
                    else:
                        print(f"Xatolik yuz berdi: {str(e)}")
        bot.send_message(chat_id,"Admin menyusi:",reply_markup=admin_panel())
                    #bot.send_message(chat_id,"Xabar barcha foydalanuchilarga yuborildi")  
    elif message.content_type == 'video' and is_admin(chat_id):
        file_id = message.video.file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)
        # Videoni admin_xabar papkasiga saqlash
        nomi=file_id[15:22]
        with open(f'admin_xabar/{nomi}.mp4', 'wb') as f:
            f.write(file)
            bot.send_message(chat_id, "Video va xabar muvaffaqiyatli saqlandi!")
        time.sleep(3)
        with open('users.txt', 'r') as file:
            users = file.readlines()
            for user in users:
                user_id = user.strip()
                try:
                    media=open(f'admin_xabar/{nomi}.mp4',"rb")
                    bot.send_video(user.strip(),video=media,caption=f"{caption}")
                except telebot.apihelper.ApiTelegramException as e:
                    if "bot was blocked by the user" in str(e):
                        print(f"User {user_id} botni bloklagan")
                    else:
                        print(f"Xatolik yuz berdi: {str(e)}")
        bot.send_message(chat_id,"Admin menyusi:",reply_markup=admin_panel())
                    #bot.send_message(chat_id,"Xabar barcha foydalanuchilarga yuborildi")  
    else:
        bot.send_message(chat_id,'bot chatiga rasm yubormang!')
@bot.message_handler(commands=['start'])
def send_start_message(message):
    with open('users.txt', 'r') as file:
        users = file.readlines()
        user_ids = [user.strip() for user in users]
    
        # Agar foydalanuvchi ID'si ro'yxatda mavjud bo'lmasa, uni saqlab qo'yamiz
        if str(message.chat.id) not in user_ids:
            with open('users.txt', 'a') as file:
                file.write(str(message.chat.id) + '\n')
    chat_id = message.chat.id
    
    if is_admin(chat_id):
        bot.send_message(chat_id,"Assalomu alaykum admin",reply_markup=admin_panel())
    else:
        user =chat_id
        channels = [bot.get_chat_member("-1001540878994", user ).status] #, bot.get_chat_member("-1001833925242", user ).status
        if channels==['member']: #, 'member'
            bot.send_message(chat_id,"Assalomu alaykum xush kelibsiz. \nInstagram video linkini yuboring !\n*Reels\n*Posts\n*Videos")
        elif channels==['creator']: #, 'creator'
            bot.send_message(chat_id,"Assalomu alaykum admin",reply_markup=admin_panel())  
        else:    
            bot.send_message(chat_id,"Assalomu alaykum botdan foydalanish uchun quyidagi kanalga a'zo bo'ling! ",reply_markup=markup)
    #bot.send_message(chat_id,  "Assalomu alaykum xush kelibsiz. \nInstagram video linkini yuboring !")

@bot.message_handler(commands=['yordam'])
def yordam(message):
    chat_id=message.chat.id
    bot.send_message(chat_id,"Quyidagi yo'naltiruchi havola orqali admin bilan bog'lanishingiz mumkin!📎",reply_markup=button_yordam())

# Linkni ozgartiruvchi funksiya
def change_link(link):
    return link.replace("www.", "dd", 1)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Linkni olish
    link = message.text
    chat_id = message.chat.id
    user = message.from_user.id
    channels = [bot.get_chat_member("-1001540878994", user ).status] #bot.get_chat_member("-1001833925242", user ).status
    if channels==['member']: #, 'member'
        if link[26:27]=='p':
            modified_link = change_link(link)
            bot.send_message(chat_id,f"<a href='{modified_link}'>Rasm</a> tayyor @Instagram_Fix_bot",parse_mode="HTML",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Ulashish↗️",url='https://t.me/Instagram_fix_bot?start=762725479')))
            bot.reply_to(message,reklama())
        elif link[26:27]=='r':
            modified_link = change_link(link)
            bot.send_message(chat_id,f"<a href='{modified_link}'>Video </a> tayyor @Instagram_Fix_bot" ,parse_mode="HTML",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Ulashish↗️",url='https://t.me/Instagram_fix_bot?start=762725479')))
            bot.reply_to(message,reklama())
        else:
            bot.reply_to(message,f"Linkni o'qiy olmadim!!\n{link}")    
     
    elif link=="Foydalanuvchilarga xabar yuborish":
        admin_xabari(message)
    elif link=='Umumiy foydalanuvchilar':
        bot.reply_to(message,f'A\'zolar: {get_user_count(file_name)} ta')    
    else:    
        bot.send_message(chat_id,"Assalomu alaykum botdan foydalanish uchun quyidagi kanalga a'zo bo'ling! ",reply_markup=markup) 
    # Foydalanuvchiga ozgartirilgan linkni yuborish
    
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check_channels(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user=call.from_user.id
    # A'zo bo'lganligini tekshirish
    channels = [bot.get_chat_member("-1001540878994", user ).status] #,bot.get_chat_member("-1001833925242", user ).status
    if channels==['member']: #, 'member'
        bot.edit_message_text(f"Xush kelibsiz! {call.from_user.first_name}\nInstagram video linkini yuboring !\n*Reels\n*Posts\n*Videos",chat_id,message_id)
    else:    
        bot.send_message(chat_id,"Kanalga a'zo bo'lmagansiz!")
    
    
# Botni ishga tushirish
bot.polling()
