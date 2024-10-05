import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import threading
from datetime import datetime, timedelta

# توكن البوت
BOT_TOKEN = '7659759330:AAFyB0vRXYWCcEnH2Df4GYVMgKzWJqVvDlU'
bot = telebot.TeleBot(BOT_TOKEN)

# قائمة التذكيرات النشطة
reminders = {}

# اللغات المتاحة
languages = ['ar', 'en']
current_language = 'ar'

# رسائل ترحيبية
welcome_messages = {
    "ar": "مرحبًا بك، {}! استخدم الأمر /help لمعرفة كيفية استخدام البوت.",
    "en": "Welcome, {}! Use the /help command to know how to use the bot."
}

# ميزة 6: رسالة ترحيبية مخصصة
@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.first_name
    bot.reply_to(message, welcome_messages[current_language].format(username))

# ميزة /help لعرض المساعدة مع أمثلة
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    الأوامر المتاحة:
    /remind <وقت> <وحدة> - تعيين تذكير بعد فترة زمنية. مثال: /remind 10 دقائق
    /cancel - إلغاء التذكير النشط.
    /list - عرض التذكيرات النشطة.
    /repeat <وقت> <وحدة> <تكرار> - تعيين تذكير متكرر. مثال: /repeat 1 ساعة يوميًا
    /remind_at <HH:MM> - تعيين تذكير في وقت محدد. مثال: /remind_at 14:00
    /remaining - عرض الوقت المتبقي للتذكير.
    /language - تغيير اللغة. مثال: /language ar
    /sound - تشغيل صوت التذكير عند انتهاء الوقت.
    /stats - عرض إحصائيات التذكيرات.
    """
    bot.reply_to(message, help_text)

# ميزة 1: تعيين تذكير
@bot.message_handler(commands=['remind'])
def set_reminder(message):
    try:
        args = message.text.split()[1:]
        time_value = int(args[0])
        time_unit = args[1].lower()

        # تحويل الوقت للوحدة المطلوبة
        if time_unit in ['دقيقة', 'دقائق', 'minutes', 'minute']:
            interval = time_value * 60
        elif time_unit in ['ساعة', 'ساعات', 'hours', 'hour']:
            interval = time_value * 3600
        else:
            bot.reply_to(message, "الوحدة الزمنية غير مدعومة. مثال: /remind 10 دقائق")
            return

        bot.reply_to(message, f"سأذكرك بعد {time_value} {time_unit}.")
        threading.Thread(target=schedule_reminder, args=(message, interval)).start()
    
    except (ValueError, IndexError):
        bot.reply_to(message, "صيغة غير صحيحة. استخدم: /remind 10 دقائق")

def schedule_reminder(message, interval):
    time.sleep(interval)
    bot.send_message(message.chat.id, "⏰ التذكير: انتهى الوقت المحدد!")

# ميزة 2: إلغاء التذكير
@bot.message_handler(commands=['cancel'])
def cancel_reminder(message):
    chat_id = message.chat.id
    if chat_id in reminders:
        reminders.pop(chat_id)
        bot.reply_to(message, "تم إلغاء التذكير!")
    else:
        bot.reply_to(message, "لا يوجد تذكير نشط.")

# ميزة 3: قائمة التذكيرات الحالية
@bot.message_handler(commands=['list'])
def list_reminders(message):
    chat_id = message.chat.id
    if chat_id in reminders:
        remaining_time = reminders[chat_id]['end_time'] - datetime.now()
        bot.reply_to(message, f"التذكير ينتهي بعد: {remaining_time}.")
    else:
        bot.reply_to(message, "لا يوجد تذكير نشط.")

# ميزة 4: تغيير اللغة باستخدام الأزرار الشفافة
@bot.message_handler(commands=['language'])
def set_language(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("العربية", callback_data="lang_ar"))
    markup.add(InlineKeyboardButton("English", callback_data="lang_en"))
    
    bot.reply_to(message, "اختر اللغة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang"))
def callback_language(call):
    global current_language
    if call.data == "lang_ar":
        current_language = "ar"
        bot.send_message(call.message.chat.id, "تم تغيير اللغة إلى العربية.")
    elif call.data == "lang_en":
        current_language = "en"
        bot.send_message(call.message.chat.id, "Language switched to English.")
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import threading
from datetime import datetime, timedelta

# توكن البوت
BOT_TOKEN = '7659759330:AAFyB0vRXYWCcEnH2Df4GYVMgKzWJqVvDlU'
bot = telebot.TeleBot(BOT_TOKEN)

# قائمة التذكيرات النشطة
reminders = {}

# اللغات المتاحة
languages = ['ar', 'en']
current_language = 'ar'

# رسائل ترحيبية
welcome_messages = {
    "ar": "مرحبًا بك، {}! استخدم الأمر /help لمعرفة كيفية استخدام البوت.",
    "en": "Welcome, {}! Use the /help command to know how to use the bot."
}

# ميزة 6: رسالة ترحيبية مخصصة
@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.first_name
    bot.reply_to(message, welcome_messages[current_language].format(username))

# ميزة /help لعرض المساعدة مع أمثلة
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    الأوامر المتاحة:
    /remind <وقت> <وحدة> - تعيين تذكير بعد فترة زمنية. مثال: /remind 10 دقائق
    /cancel - إلغاء التذكير النشط.
    /list - عرض التذكيرات النشطة.
    /repeat <وقت> <وحدة> <تكرار> - تعيين تذكير متكرر. مثال: /repeat 1 ساعة يوميًا
    /remind_at <HH:MM> - تعيين تذكير في وقت محدد. مثال: /remind_at 14:00
    /remaining - عرض الوقت المتبقي للتذكير.
    /language - تغيير اللغة. مثال: /language ar
    /sound - تشغيل صوت التذكير عند انتهاء الوقت.
    /stats - عرض إحصائيات التذكيرات.
    """
    bot.reply_to(message, help_text)

# ميزة 1: تعيين تذكير
@bot.message_handler(commands=['remind'])
def set_reminder(message):
    try:
        args = message.text.split()[1:]
        time_value = int(args[0])
        time_unit = args[1].lower()

        # تحويل الوقت للوحدة المطلوبة
        if time_unit in ['دقيقة', 'دقائق', 'minutes', 'minute']:
            interval = time_value * 60
        elif time_unit in ['ساعة', 'ساعات', 'hours', 'hour']:
            interval = time_value * 3600
        else:
            bot.reply_to(message, "الوحدة الزمنية غير مدعومة. مثال: /remind 10 دقائق")
            return

        bot.reply_to(message, f"سأذكرك بعد {time_value} {time_unit}.")
        threading.Thread(target=schedule_reminder, args=(message, interval)).start()
    
    except (ValueError, IndexError):
        bot.reply_to(message, "صيغة غير صحيحة. استخدم: /remind 10 دقائق")

def schedule_reminder(message, interval):
    time.sleep(interval)
    bot.send_message(message.chat.id, "⏰ التذكير: انتهى الوقت المحدد!")

# ميزة 2: إلغاء التذكير
@bot.message_handler(commands=['cancel'])
def cancel_reminder(message):
    chat_id = message.chat.id
    if chat_id in reminders:
        reminders.pop(chat_id)
        bot.reply_to(message, "تم إلغاء التذكير!")
    else:
        bot.reply_to(message, "لا يوجد تذكير نشط.")

# ميزة 3: قائمة التذكيرات الحالية
@bot.message_handler(commands=['list'])
def list_reminders(message):
    chat_id = message.chat.id
    if chat_id in reminders:
        remaining_time = reminders[chat_id]['end_time'] - datetime.now()
        bot.reply_to(message, f"التذكير ينتهي بعد: {remaining_time}.")
    else:
        bot.reply_to(message, "لا يوجد تذكير نشط.")

# ميزة 4: تغيير اللغة باستخدام الأزرار الشفافة
@bot.message_handler(commands=['language'])
def set_language(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("العربية", callback_data="lang_ar"))
    markup.add(InlineKeyboardButton("English", callback_data="lang_en"))
    
    bot.reply_to(message, "اختر اللغة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang"))
def callback_language(call):
    global current_language
    if call.data == "lang_ar":
        current_language = "ar"
        bot.send_message(call.message.chat.id, "تم تغيير اللغة إلى العربية.")
    elif call.data == "lang_en":
        current_language = "en"
        bot.send_message(call.message.chat.id, "Language switched to English.")
    bot.answer_callback_query(call.id)

# ميزة 5: عرض إحصائيات المستخدم
@bot.message_handler(commands=['stats'])
def user_stats(message):
    bot.reply_to(message, f"لقد قمت بتعيين {len(reminders)} تذكيرات حتى الآن!")

# ميزة 6: تشغيل صوت التذكير
@bot.message_handler(commands=['sound'])
def play_reminder_sound(message):
    bot.reply_to(message, "📢 سيتم تشغيل صوت التذكير!")
    bot.send_audio(message.chat.id, open('reminder_sound.mp3', 'rb'))

# ميزة 7: تعيين تذكير في وقت محدد
@bot.message_handler(commands=['remind_at'])
def remind_at(message):
    try:
        args = message.text.split()[1:]
        time_str = args[0]
        reminder_time = datetime.strptime(time_str, '%H:%M').time()

        now = datetime.now()
        reminder_datetime = datetime.combine(now, reminder_time)

        if reminder_datetime < now:
            reminder_datetime += timedelta(days=1)

        interval = (reminder_datetime - now).total_seconds()
        bot.reply_to(message, f"سيتم تذكيرك في {time_str}.")
        threading.Thread(target=schedule_reminder, args=(message, interval)).start()

    except (ValueError, IndexError):
        bot.reply_to(message, "صيغة غير صحيحة. استخدم: /remind_at 14:00")

# ميزة 8: تذكير متكرر
@bot.message_handler(commands=['repeat'])
def repeat_reminder(message):
    try:
        args = message.text.split()[1:]
        time_value = int(args[0])
        time_unit = args[1].lower()
        repeat_interval = int(args[2])

        if time_unit in ['دقيقة', 'دقائق', 'minutes', 'minute']:
            interval = time_value * 60
        elif time_unit in ['ساعة', 'ساعات', 'hours', 'hour']:
            interval = time_value * 3600
        else:
            bot.reply_to(message, "الوحدة الزمنية غير مدعومة. مثال: /repeat 1 ساعة يوميًا")
            return

        bot.reply_to(message, f"سيتم تذكيرك كل {time_value} {time_unit}.")
        threading.Thread(target=schedule_repeat_reminder, args=(message, interval, repeat_interval)).start()

    except (ValueError, IndexError):
        bot.reply_to(message, "صيغة غير صحيحة. استخدم: /repeat 1 ساعة يوميًا")

def schedule_repeat_reminder(message, interval, repeat_interval):
    while repeat_interval > 0:
        time.sleep(interval)
        bot.send_message(message.chat.id, "⏰ التذكير المتكرر!")
        repeat_interval -= 1

# ميزة 9: عرض الوقت المتبقي للتذكير
@bot.message_handler(commands=['remaining'])
def remaining_time(message):
    chat_id = message.chat.id
    if chat_id in reminders:
        remaining_time = reminders[chat_id]['end_time'] - datetime.now()
        bot.reply_to(message, f"الوقت المتبقي للتذكير: {remaining_time}.")
    else:
        bot.reply_to(message, "لا يوجد تذكير نشط.")

# ميزة 10: رسالة تأكيد بعد كل أمر
def send_confirmation(message, text):
    bot.reply_to(message, f"{text} ✅")

# تشغيل البوت
bot.polling()￼Enter    bot.answer_callback_query(call.id)

# ميزة 5: عرض إحصائيات المستخدم
@bot.message_handler(commands=['stats'])
def user_stats(message):
    bot.reply_to(message, f"لقد قمت بتعيين {len(reminders)} تذكيرات حتى الآن!")

# ميزة 6: تشغيل صوت التذكير
@bot.message_handler(commands=['sound'])
def play_reminder_sound(message):
    bot.reply_to(message, "📢 سيتم تشغيل صوت التذكير!")
    bot.send_audio(message.chat.id, open('reminder_sound.mp3', 'rb'))

# ميزة 7: تعيين تذكير في وقت محدد
@bot.message_handler(commands=['remind_at'])
def remind_at(message):
    try:
        args = message.text.split()[1:]
        time_str = args[0]
        reminder_time = datetime.strptime(time_str, '%H:%M').time()

        now = datetime.now()
        reminder_datetime = datetime.combine(now, reminder_time)

        if reminder_datetime < now:
            reminder_datetime += timedelta(days=1)
   interval = (reminder_datetime - now).total_seconds()
        bot.reply_to(message, f"سيتم تذكيرك في {time_str}.")
        threading.Thread(target=schedule_reminder, args=(message, interval)).start()

    except (ValueError, IndexError):
        bot.reply_to(message, "صيغة غير صحيحة. استخدم: /remind_at 14:00")

# ميزة 8: تذكير متكرر
@bot.message_handler(commands=['repeat'])
def repeat_reminder(message):
    try:
        args = message.text.split()[1:]
        time_value = int(args[0])
        time_unit = args[1].lower()
        repeat_interval = int(args[2])

        if time_unit in ['دقيقة', 'دقائق', 'minutes', 'minute']:
            interval = time_value * 60
        elif time_unit in ['ساعة', 'ساعات', 'hours', 'hour']:
            interval = time_value * 3600
        else:
            bot.reply_to(message, "الوحدة الزمنية غير مدعومة. مثال: /repeat 1 ساعة يوميًا")
            return

        bot.reply_to(message, f"سيتم تذكيرك كل {time_value} {time_unit}.")
