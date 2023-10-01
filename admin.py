from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup
from telebot.util import quick_markup
markup = quick_markup({
        '📎Obuna bo\'ling': {'url': 'https://t.me/LOADING_My_point'}, #'📎Obuna bo\'ling': {'url': 'https://t.me/Abbosbek_coder'},
        'Tekshirish ✅': {'callback_data': 'check'} 
    }, row_width=1)

def is_admin(user_id):
    admins = [762725479]  # adminlar ro'yxati
    return user_id in admins
def reklama():
    xabar="@Instagram_Fix_bot orqali videolarni oson yuklang."
    return xabar
def admin_panel():
    panel=ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
    ad1=KeyboardButton("Foydalanuvchilarga xabar yuborish")
    ad2=KeyboardButton('Umumiy foydalanuvchilar')
    panel.add(ad1,ad2)
    return panel
def button_yordam():
    button_yor=InlineKeyboardMarkup()
    admin=InlineKeyboardButton("Bot admin",url="t.me/Abbosbek_Turdaliyev")
    button_yor.add(admin)
    return button_yor
