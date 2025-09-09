import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, FloodWaitError, PhoneNumberInvalidError
from telethon.sync import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateUsernameRequest
import asyncio
import os
import json
import threading
import re
import random
import time
import sys
import requests

# إعدادات API
API_ID = 20170078
API_HASH = "f5f0c975f404d080cb2a0e993a7f591f"
TOKEN = "8308025373:AAGi4Zu-rBj8FJutsbFUxBhlNhfcmNzSivM"

# أسماء الملفات
USERS_FILE = "users.json"
SESSIONS_FILE = "Sin.txt"

# تهيئة الكائنات العامة
clients = {}
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot = telebot.TeleBot(TOKEN)
posting_active = {}  # لتتبع حالة النشر لكل مستخدم
user_messages = {}  # لتخزين رسائل المستخدمين لحذفها لاحقاً

print("تم تشغيل البوت بنجاح")

def run_loop():
    """تشغيل حلقة الأحداث بشكل منفصل"""
    loop.run_forever()

# تشغيل حلقة الأحداث في خلفية منفصلة
threading.Thread(target=run_loop, daemon=True).start()

def load_data(filename, default_value={}):
    """تحميل البيانات من ملف JSON"""
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(default_value, f)
        return default_value
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                new_data = {}
                for i, item in enumerate(data):
                    new_data[str(i)] = item
                save_data(filename, new_data)
                return new_data
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return default_value

def save_data(filename, data):
    """حفظ البيانات إلى ملف JSON"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_session_to_file(user_id, session_str):
    """حفظ الجلسة في ملف النص"""
    with open(SESSIONS_FILE, "a", encoding="utf-8") as f:
        f.write(f"User ID: {user_id}\nSession: {session_str}\n\n")

def ensure_user(user_id):
    """التأكد من وجود المستخدم في قاعدة البيانات"""
    users = load_data(USERS_FILE)
    user_id_str = str(user_id)
    
    if user_id_str not in users:
        users[user_id_str] = {
            "settings": {
                "time": 300,  # زيادة الوقت إلى 5 دقائق بين الرسائل
                "send": 1,    # تقليل عدد الرسائل إلى 1 فقط
                "super": [],
                "message": "",
                "auto_change": False
            },
            "sessions": {},
            "posting_active": False,
            "last_action_time": 0  # وقت آخر عملية لتجنب التكرار السريع
        }
        save_data(USERS_FILE, users)
    
    return users[user_id_str]

def create_client(session_str=None):
    """إنشاء عميل تليجرام بإعدادات أكثر أماناً"""
    # إعدادات عشوائية لتجنب الكشف
    devices = [
        {"model": "Samsung Galaxy S21", "version": "12.0", "app": "9.4.0"},
        {"model": "iPhone 13 Pro", "version": "15.0", "app": "9.4.0"},
        {"model": "Xiaomi Mi 11", "version": "11.0", "app": "9.3.0"},
        {"model": "Google Pixel 6", "version": "13.0", "app": "9.2.0"},
    ]
    
    device = random.choice(devices)
    
    return TelegramClient(
        StringSession(session_str) if session_str else StringSession(),
        api_id=API_ID,
        api_hash=API_HASH,
        device_model=device["model"],
        system_version=device["version"],
        app_version=device["app"],
        loop=loop
    )

def create_main_menu():
    """إنشاء قائمة رئيسية"""
    markup = InlineKeyboardMarkup(row_width=2)
    
    markup.add(
        InlineKeyboardButton(text="🔐 تسجيل الدخول", callback_data="login"),
        InlineKeyboardButton(text="📝 الرسالة", callback_data="mes"),
        InlineKeyboardButton(text="🔗 الروابط", callback_data="super"),
        InlineKeyboardButton(text="⏱️ الوقت", callback_data="time"),
        InlineKeyboardButton(text="🔢 العدد", callback_data="send"),
        InlineKeyboardButton(text="▶️ بدء النشر", callback_data="start_posting"),
        InlineKeyboardButton(text="⏹️ إيقاف النشر", callback_data="stop_posting"),
        InlineKeyboardButton(text="❓ المساعدة", callback_data="help"),
        InlineKeyboardButton(text="📞 المطور", url="https://t.me/F_51c")
    )
    
    return markup

def delete_user_messages(chat_id):
    """حذف رسائل المستخدم القديمة"""
    if chat_id in user_messages:
        for msg_id in user_messages[chat_id]:
            try:
                bot.delete_message(chat_id, msg_id)
            except:
                pass
        user_messages[chat_id] = []

def schedule_message_deletion(chat_id, message_id, delay=2.0):  # زيادة التأخير إلى 2 ثانية
    """جدولة حذف الرسالة بعد تأخير"""
    def delete_message():
        time.sleep(delay)
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
    
    threading.Thread(target=delete_message, daemon=True).start()

@bot.message_handler(commands=["start"])
def start(message):
    """معالجة أمر البدء"""
    user_data = ensure_user(message.from_user.id)
    delete_user_messages(message.chat.id)
    
    welcome_text = """
<b>مرحباً بك أيها المستخدم الكريم!</b> 

<b>أنا بوت النشر التلقائي للتيليجرام، أساعدك في نشر رسائلك تلقائياً في القنوات والمجموعات.</b>

<b>⚠️ نصائح أمان مهمة:</b>
<b>•</b> <i>استخدم وقتاً كافياً بين الرسائل (5 دقائق على الأقل)</i>
<b>•</b> <i>لا ترسل أكثر من رسالة واحدة في الجلسة الواحدة</i>
<b>•</b> <i>تجنب إرسال الرسائل بسرعة كبيرة</i>
<b>•</b> <i>لا تستخدم البوت بشكل مكثف في فترات زمنية قصيرة</i>

<b>اختر أحد الخيارات من القائمة أدناه للبدء:</b>
"""
    
    try:
        sent_msg = bot.send_photo(
            message.chat.id,
            photo="https://t.me/u7uu7ui/57",
            caption=welcome_text,
            reply_markup=create_main_menu(),
            parse_mode="HTML"
        )
        if message.chat.id not in user_messages:
            user_messages[message.chat.id] = []
        user_messages[message.chat.id].append(sent_msg.message_id)
    except Exception as e:
        print(f"خطأ في إرسال الصورة: {e}")
        sent_msg = bot.send_message(
            message.chat.id,
            welcome_text,
            reply_markup=create_main_menu(),
            parse_mode="HTML"
        )
        if message.chat.id not in user_messages:
            user_messages[message.chat.id] = []
        user_messages[message.chat.id].append(sent_msg.message_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """معالجة استدعاءات الأزرار"""
    user_id = str(call.from_user.id)
    users = ensure_user(user_id)
    
    # التحقق من الوقت بين العمليات لتجنب التكرار السريع
    current_time = time.time()
    if current_time - users.get("last_action_time", 0) < 2:  # انتظار ثانيتين بين العمليات
        bot.answer_callback_query(call.id, "⏳ يرجى الانتظار قليلاً قبل القيام بعملية أخرى", show_alert=True)
        return
    
    users["last_action_time"] = current_time
    save_data(USERS_FILE, users)
    
    delete_user_messages(call.message.chat.id)
    
    if call.data == "mes":
        ask_for_message(call)
    elif call.data == "send":
        ask_for_send_count(call)
    elif call.data == "super":
        ask_for_super_links(call)
    elif call.data == "time":
        ask_for_time(call)
    elif call.data == "login":
        ask_for_phone(call)
    elif call.data == "start_posting":
        start_posting(call)
    elif call.data == "stop_posting":
        stop_posting(call)
    elif call.data == "help":
        show_help(call)
    elif call.data == "back":
        go_back(call)
    else:
        bot.answer_callback_query(call.id, "هذا الزر غير معروف", show_alert=True)

def show_help(call):
    """عرض رسالة المساعدة"""
    help_text = """
<b>دليل استخدام البوت:</b>

<b>1. 🔐 تسجيل الدخول:</b> <i>إضافة حسابك عن طريق رقم الهاتف</i>
<b>2. 📝 الرسالة:</b> <i>تحديد الرسالة التي تريد نشرها</i>
<b>3. 🔗 الروابط:</b> <i>إضافة روابط المجموعات والقنوات المستهدفة</i>
<b>4. ⏱️ الوقت:</b> <i>ضبط الوقت بين كل رسالة (300 ثانية على الأقل)</i>
<b>5. 🔢 العدد:</b> <i>تحديد عدد المرات التي ترسل فيها الرسالة (1 فقط)</i>
<b>6. ▶️ بدء النشر:</b> <i>بدء عملية النشر التلقائي</i>
<b>7. ⏹️ إيقاف النشر:</b> <i>إيقاف عملية النشر</i>

<b>نصائح أمان مهمة:</b>
<b>•</b> <i>استخدم وقتاً كافياً بين الرسائل (5 دقائق على الأقل)</i>
<b>•</b> <i>لا ترسل أكثر من رسالة واحدة في الجلسة الواحدة</i>
<b>•</b> <i>تجنب إرسال الرسائل بسرعة كبيرة</i>
<b>•</b> <i>لا تستخدم البوت بشكل مكثف في فترات زمنية قصيرة</i>

<b>كيفية إرسال روابط السوبر:</b>
<b>1.</b> <i>انسخ رابط المجموعة أو القناة</i>
<b>2.</b> <i>أرسل الروابط كل رابط في سطر منفصل</i>
<b>3.</b> <i>مثال:</i>
<code>https://t.me/group1
https://t.me/group2
https://t.me/group3</code>

<b>الحد الأقصى: 10 روابط فقط للحماية من الحظر</b>
"""
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="العودة للقائمة الرئيسية", callback_data="back"))
    
    try:
        sent_msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=help_text,
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    except:
        sent_msg = bot.send_message(
            call.message.chat.id,
            help_text,
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)

def ask_for_message(call):
    """الطلب لإدخال الرسالة"""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    try:
        sent_msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="<b>أرسل الرسالة التي تريد نشرها في القنوات والمجموعات</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    except:
        sent_msg = bot.send_message(
            call.message.chat.id,
            "<b>أرسل الرسالة التي تريد نشرها في القنوات والمجموعات</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    
    bot.register_next_step_handler(call.message, save_message)

def ask_for_send_count(call):
    """الطلب لإدخال عدد مرات الإرسال"""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    try:
        sent_msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="<b>أرسل عدد المرات التي تريد إرسال الرسالة فيها (1 فقط للحماية من الحظر)</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    except:
        sent_msg = bot.send_message(
            call.message.chat.id,
            "<b>أرسل عدد المرات التي تريد إرسال الرسالة فيها (1 فقط للحماية من الحظر)</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    
    bot.register_next_step_handler(call.message, save_send_count)

def ask_for_super_links(call):
    """الطلب لإدخال الروابط السوبر"""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    help_text = """
<b>كيفية إرسال روابط السوبر:</b>
<b>1.</b> <i>انسخ رابط المجموعة أو القناة</i>
<b>2.</b> <i>أرسل الروابط كل رابط في سطر منفصل</i>
<b>3.</b> <i>مثال:</i>
<code>https://t.me/group1
https://t.me/group2
https://t.me/group3</code>

<b>الحد الأقصى: 10 روابط فقط للحماية من الحظر</b>
"""
    
    try:
        sent_msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=help_text,
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    except:
        sent_msg = bot.send_message(
            call.message.chat.id,
            help_text,
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    
    bot.register_next_step_handler(call.message, save_super_links)

def ask_for_time(call):
    """الطلب لإدخال الوقت"""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    try:
        sent_msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="<b>أرسل الوقت بين كل رسالة بالثواني (300 ثانية على الأقل - 5 دقائق)</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    except:
        sent_msg = bot.send_message(
            call.message.chat.id,
            "<b>أرسل الوقت между كل رسالة بالثواني (300 ثانية على الأقل - 5 دقائق)</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    
    bot.register_next_step_handler(call.message, save_time)

def ask_for_phone(call):
    """الطلب لإدخال رقم الهاتف"""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    try:
        sent_msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="<b>أرسل رقم هاتفك مع رمز الدولة (مثال: +1234567890)</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    except:
        sent_msg = bot.send_message(
            call.message.chat.id,
            "<b>أرسل رقم هاتفك مع رمز الدولة (مثال: +1234567890)</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    
    bot.register_next_step_handler(call.message, process_phone)

def start_posting(call):
    """بدء عملية النشر"""
    users = load_data(USERS_FILE)
    user_id = str(call.from_user.id)
    
    if user_id not in users or not users[user_id].get("sessions"):
        bot.answer_callback_query(call.id, "يجب تسجيل الدخول أولاً", show_alert=True)
        return
    
    users[user_id]["posting_active"] = True
    save_data(USERS_FILE, users)
    posting_active[user_id] = True
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    try:
        sent_msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="<b>جاري البدء في النشر...</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    except:
        sent_msg = bot.send_message(
            call.message.chat.id,
            "<b>جاري البدء في النشر...</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    
    asyncio.run_coroutine_threadsafe(run_posting(user_id, call.message.chat.id), loop)

def stop_posting(call):
    """إيقاف عملية النشر"""
    users = load_data(USERS_FILE)
    user_id = str(call.from_user.id)
    
    if user_id in users:
        users[user_id]["posting_active"] = False
        save_data(USERS_FILE, users)
    
    if user_id in posting_active:
        posting_active[user_id] = False
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    try:
        sent_msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="<b>تم إيقاف النشر بنجاح</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    except:
        sent_msg = bot.send_message(
            call.message.chat.id,
            "<b>تم إيقاف النشر بنجاح</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)

def go_back(call):
    """العودة للقائمة الرئيسية"""
    welcome_text = """
<b>مرحباً بك أيها المستخدم الكريم!</b> 

<b>أنا بوت النشر التلقائي للتيليجرام، أساعدك في نشر رسائلك تلقائياً في القنوات والمجموعات.</b>

<b>⚠️ نصائح أمان مهمة:</b>
<b>•</b> <i>استخدم وقتاً كافياً بين الرسائل (5 دقائق على الأقل)</i>
<b>•</b> <i>لا ترسل أكثر من رسالة واحدة في الجلسة الواحدة</i>
<b>•</b> <i>تجنب إرسال الرسائل بسرعة كبيرة</i>
<b>•</b> <i>لا تستخدم البوت بشكل مكثف في فترات زمنية قصيرة</i>

<b>اختر أحد الخيارات من القائمة أدناه للبدء:</b>
"""
    
    try:
        sent_msg = bot.send_photo(
            call.message.chat.id,
            photo="https://i.imgur.com/OXXAe66.jpeg",
            caption=welcome_text,
            reply_markup=create_main_menu(),
            parse_mode="HTML"
        )
        if call.message.chat.id not in user_messages:
            user_messages[call.message.chat.id] = []
        user_messages[call.message.chat.id].append(sent_msg.message_id)
    except Exception as e:
        print(f"خطأ في إرسال الصورة: {e}")
        try:
            sent_msg = bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=welcome_text,
                reply_markup=create_main_menu(),
                parse_mode="HTML"
            )
            if call.message.chat.id not in user_messages:
                user_messages[call.message.chat.id] = []
            user_messages[call.message.chat.id].append(sent_msg.message_id)
        except:
            sent_msg = bot.send_message(
                call.message.chat.id,
                welcome_text,
                reply_markup=create_main_menu(),
                parse_mode="HTML"
            )
            if call.message.chat.id not in user_messages:
                user_messages[call.message.chat.id] = []
            user_messages[call.message.chat.id].append(sent_msg.message_id)

def save_message(message):
    """حفظ الرسالة"""
    user_id = str(message.from_user.id)
    users = load_data(USERS_FILE)
    
    # حذف الرسالة بعد 2 ثانية
    schedule_message_deletion(message.chat.id, message.message_id, 2.0)
    
    if user_id in users:
        users[user_id]["settings"]["message"] = message.text
        save_data(USERS_FILE, users)
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    sent_msg = bot.reply_to(message, "<b>تم حفظ الرسالة بنجاح</b>", reply_markup=markup, parse_mode="HTML")
    if message.chat.id not in user_messages:
        user_messages[message.chat.id] = []
    user_messages[message.chat.id].append(sent_msg.message_id)

def save_send_count(message):
    """حفظ عدد مرات الإرسال"""
    user_id = str(message.from_user.id)
    users = load_data(USERS_FILE)
    
    # حذف الرسالة بعد 2 ثانية
    schedule_message_deletion(message.chat.id, message.message_id, 2.0)
    
    if user_id in users and message.text.isdigit():
        send_count = int(message.text)
        if send_count > 1:  # الحد الأقصى هو 1 فقط
            send_count = 1
            response = "<b>تم تحديد العدد إلى 1 كحد أقصى للحماية من الحظر</b>"
        else:
            response = f"<b>تم تعيين عدد المرات إلى: {send_count}</b>"
        
        users[user_id]["settings"]["send"] = send_count
        save_data(USERS_FILE, users)
    else:
        response = "<b>خطأ: يجب إدخال رقم صحيح</b>"
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    sent_msg = bot.reply_to(message, response, reply_markup=markup, parse_mode="HTML")
    if message.chat.id not in user_messages:
        user_messages[message.chat.id] = []
    user_messages[message.chat.id].append(sent_msg.message_id)

def save_super_links(message):
    """حفظ الروابط السوبر"""
    user_id = str(message.from_user.id)
    users = load_data(USERS_FILE)
    
    # حذف الرسالة بعد 2 ثانية
    schedule_message_deletion(message.chat.id, message.message_id, 2.0)
    
    if user_id in users:
        links = [link.strip() for link in message.text.split('\n') if link.strip()]
        
        if len(links) > 10:  # تقليل الحد الأقصى إلى 10 روابط فقط
            links = links[:10]
            response = f"<b>تم حفظ أول 10 روابط فقط للحماية من الحظر\nتم حفظ {len(links)} روابط بنجاح</b>"
        else:
            response = f"<b>تم حفظ {len(links)} روابط بنجاح</b>"
        
        users[user_id]["settings"]["super"] = links
        save_data(USERS_FILE, users)
    else:
        response = "<b>خطأ: لم يتم العثور على بيانات المستخدم</b>"
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    sent_msg = bot.reply_to(message, response, reply_markup=markup, parse_mode="HTML")
    if message.chat.id not in user_messages:
        user_messages[message.chat.id] = []
    user_messages[message.chat.id].append(sent_msg.message_id)

def save_time(message):
    """حفظ الوقت"""
    user_id = str(message.from_user.id)
    users = load_data(USERS_FILE)
    
    # حذف الرسالة بعد 2 ثانية
    schedule_message_deletion(message.chat.id, message.message_id, 2.0)
    
    if user_id in users and message.text.isdigit():
        time_val = int(message.text)
        if time_val < 300:  # 5 دقائق كحد أدنى
            time_val = 300
            response = "<b>تم تحديد الوقت إلى 300 ثانية كحد أدنى للحماية من الحظر</b>"
        else:
            response = f"<b>تم تعيين الوقت إلى: {time_val} ثانية</b>"
        
        users[user_id]["settings"]["time"] = time_val
        save_data(USERS_FILE, users)
    else:
        response = "<b>خطأ: يجب إدخال رقم صحيح</b>"
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
    
    sent_msg = bot.reply_to(message, response, reply_markup=markup, parse_mode="HTML")
    if message.chat.id not in user_messages:
        user_messages[message.chat.id] = []
    user_messages[message.chat.id].append(sent_msg.message_id)

def process_phone(message):
    """معالجة رقم الهاتف"""
    phone = message.text.strip()
    
    # حذف الرسالة بعد 2 ثانية
    schedule_message_deletion(message.chat.id, message.message_id, 2.0)
    
    if not re.match(r'^\+\d{10,15}$', phone):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
        
        sent_msg = bot.reply_to(message, "<b>رقم الهاتف غير صحيح. يجب أن يبدأ بـ + ويتبعه أرقام</b>", reply_markup=markup, parse_mode="HTML")
        if message.chat.id not in user_messages:
            user_messages[message.chat.id] = []
        user_messages[message.chat.id].append(sent_msg.message_id)
        return
    
    asyncio.run_coroutine_threadsafe(send_code_request(phone, message.chat.id), loop)

async def send_code_request(phone, chat_id):
    """إرسال طلب الكود"""
    try:
        client = create_client()
        await client.connect()
        await client.send_code_request(phone=phone)
        clients[chat_id] = client
        
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
        
        sent_msg = bot.send_message(chat_id, "<b>تم إرسال الكود، يرجى إدخال الكود (مثال: 1 2 3 4 5)</b>", reply_markup=markup, parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)
        bot.register_next_step_handler_by_chat_id(chat_id, lambda msg: process_code(msg, phone))
    except FloodWaitError as e:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
        
        sent_msg = bot.send_message(chat_id, f"<b>يجب الانتظار {e.seconds} ثانية قبل المحاولة مرة أخرى</b>", reply_markup=markup, parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)
    except PhoneNumberInvalidError:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
        
        sent_msg = bot.send_message(chat_id, "<b>رقم الهاتف غير صحيح</b>", reply_markup=markup, parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)
    except Exception as e:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
        
        sent_msg = bot.send_message(chat_id, f"<b>خطأ: {str(e)}</b>", reply_markup=markup, parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)

def process_code(message, phone):
    """معالجة الكود المرسل"""
    code = message.text.strip().replace(" ", "")
    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    
    # حذف الرسالة بعد 2 ثانية
    schedule_message_deletion(message.chat.id, message.message_id, 2.0)
    
    asyncio.run_coroutine_threadsafe(check_code(phone, code, chat_id, user_id), loop)

async def check_code(phone, code, chat_id, user_id):
    """التحقق من الكود"""
    users = load_data(USERS_FILE)
    
    try:
        client = clients[chat_id]
        await client.sign_in(phone=phone, code=code)
        session = client.session.save()
        
        if user_id not in users:
            users[user_id] = {"settings": {}, "sessions": {}, "posting_active": False}
        
        if "sessions" not in users[user_id]:
            users[user_id]["sessions"] = {}
        
        session_key = f"session{len(users[user_id]['sessions']) + 1}"
        users[user_id]["sessions"][session_key] = session
        save_data(USERS_FILE, users)
        
        save_session_to_file(user_id, session)
        
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
        
        sent_msg = bot.send_message(chat_id, "<b>تم حفظ الجلسة بنجاح</b>", reply_markup=markup, parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)
    except SessionPasswordNeededError:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
        
        sent_msg = bot.send_message(chat_id, "<b>يطلب الحساب كلمة مرور ثنائية، يرجى إدخالها</b>", reply_markup=markup, parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)
        bot.register_next_step_handler_by_chat_id(chat_id, lambda msg: process_password(msg, phone))
    except Exception as e:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
        
        sent_msg = bot.send_message(chat_id, f"<b>كود غير صحيح. الخطأ: {str(e)}</b>", reply_markup=markup, parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)

def process_password(message, phone):
    """معالجة كلمة المرور"""
    password = message.text.strip()
    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    
    # حذف الرسالة بعد 2 ثانية
    schedule_message_deletion(message.chat.id, message.message_id, 2.0)
    
    asyncio.run_coroutine_threadsafe(check_password(chat_id, password, user_id), loop)

async def check_password(chat_id, password, user_id):
    """التحقق من كلمة المرور"""
    users = load_data(USERS_FILE)
    
    try:
        client = clients[chat_id]
        await client.sign_in(password=password)
        session = client.session.save()
        
        if user_id not in users:
            users[user_id] = {"settings": {}, "sessions": {}, "posting_active": False}
        
        if "sessions" not in users[user_id]:
            users[user_id]["sessions"] = {}
        
        session_key = f"session{len(users[user_id]['sessions']) + 1}"
        users[user_id]["sessions"][session_key] = session
        save_data(USERS_FILE, users)
        
        save_session_to_file(user_id, session)
        
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
        
        sent_msg = bot.send_message(chat_id, "<b>تم حفظ الجلسة بنجاح</b>", reply_markup=markup, parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)
    except Exception as e:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="العودة", callback_data="back"))
        
        sent_msg = bot.send_message(chat_id, f"<b>كلمة مرور خاطئة. الخطأ: {str(e)}</b>", reply_markup=markup, parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)

async def run_posting(user_id, chat_id):
    """تشغيل عملية النشر"""
    users = load_data(USERS_FILE)
    
    if user_id not in users:
        sent_msg = bot.send_message(chat_id, "<b>لم يتم العثور على بيانات المستخدم</b>", parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)
        return
    
    user_data = users[user_id]
    settings = user_data.get("settings", {})
    sessions = user_data.get("sessions", {})
    
    required_settings = ["time", "send", "super", "message"]
    missing_settings = [setting for setting in required_settings if not settings.get(setting)]
    
    if missing_settings:
        sent_msg = bot.send_message(
            chat_id, 
            f"<b>الإعدادات غير مكتملة. الإعدادات الناقصة: {', '.join(missing_settings)}</b>",
            parse_mode="HTML"
        )
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)
        return
    
    if not sessions:
        sent_msg = bot.send_message(chat_id, "<b>لا توجد جلسات مسجلة</b>", parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)
        return
    
    try:
        time_val = int(settings["time"])
        send_count = int(settings["send"])
        super_links = settings["super"]
        message_text = settings["message"]
        
        if not isinstance(super_links, list):
            super_links = [super_links]
        
        sent_any = False
        
        for session_name, session_str in sessions.items():
            if not posting_active.get(user_id, True):
                sent_msg = bot.send_message(chat_id, "<b>تم إيقاف النشر</b>", parse_mode="HTML")
                if chat_id not in user_messages:
                    user_messages[chat_id] = []
                user_messages[chat_id].append(sent_msg.message_id)
                return
                
            try:
                client = create_client(session_str)
                await client.connect()
                
                # إضافة تأخير عشوائي قبل البدء
                await asyncio.sleep(random.randint(10, 30))
                
                for link in super_links:
                    if not posting_active.get(user_id, True):
                        sent_msg = bot.send_message(chat_id, "<b>تم إيقاف النشر</b>", parse_mode="HTML")
                        if chat_id not in user_messages:
                            user_messages[chat_id] = []
                        user_messages[chat_id].append(sent_msg.message_id)
                        await client.disconnect()
                        return
                        
                    try:
                        entity = await client.get_entity(link)
                        
                        for i in range(send_count):
                            if not posting_active.get(user_id, True):
                                sent_msg = bot.send_message(chat_id, "<b>تم إيقاف النشر</b>", parse_mode="HTML")
                                if chat_id not in user_messages:
                                    user_messages[chat_id] = []
                                user_messages[chat_id].append(sent_msg.message_id)
                                await client.disconnect()
                                return
                                
                            try:
                                # إضافة تأخير عشوائي قبل الإرسال
                                await asyncio.sleep(random.randint(5, 15))
                                
                                await client.send_message(entity, message_text)
                                sent_any = True
                                
                                # إرسال تقرير بنجاح الإرسال
                                sent_msg = bot.send_message(chat_id, f"<b>تم الإرسال إلى {link} بنجاح</b>", parse_mode="HTML")
                                if chat_id not in user_messages:
                                    user_messages[chat_id] = []
                                user_messages[chat_id].append(sent_msg.message_id)
                                
                                if i < send_count - 1:
                                    # استخدام وقت انتظار أطول مع عشوائية
                                    random_delay = random.randint(time_val, time_val + 120)
                                    await asyncio.sleep(random_delay)
                                    
                            except FloodWaitError as e:
                                sent_msg = bot.send_message(chat_id, f"<b>يجب الانتظار {e.seconds} ثانية بسبب FloodWait</b>", parse_mode="HTML")
                                if chat_id not in user_messages:
                                    user_messages[chat_id] = []
                                user_messages[chat_id].append(sent_msg.message_id)
                                await asyncio.sleep(e.seconds + 60)  # زيادة وقت الانتظار
                            except Exception as e:
                                sent_msg = bot.send_message(chat_id, f"<b>خطأ في الإرسال: {str(e)}</b>", parse_mode="HTML")
                                if chat_id not in user_messages:
                                    user_messages[chat_id] = []
                                user_messages[chat_id].append(sent_msg.message_id)
                                await asyncio.sleep(120)  # زيادة وقت الانتظار عند الخطأ
                                
                        if link != super_links[-1]:
                            # زيادة وقت الانتظار بين الروابط
                            await asyncio.sleep(random.randint(120, 300))
                            
                    except Exception as e:
                        sent_msg = bot.send_message(chat_id, f"<b>خطأ في الرابط {link}: {str(e)}</b>", parse_mode="HTML")
                        if chat_id not in user_messages:
                            user_messages[chat_id] = []
                        user_messages[chat_id].append(sent_msg.message_id)
                        await asyncio.sleep(120)  # زيادة وقت الانتظار عند الخطأ
                
                await client.disconnect()
                
                if len(sessions) > 1:
                    # زيادة وقت الانتظار بين الجلسات
                    await asyncio.sleep(random.randint(600, 1200))
                    
            except Exception as e:
                sent_msg = bot.send_message(chat_id, f"<b>خطأ في الجلسة {session_name}: {str(e)}</b>", parse_mode="HTML")
                if chat_id not in user_messages:
                    user_messages[chat_id] = []
                user_messages[chat_id].append(sent_msg.message_id)
                await asyncio.sleep(300)  # زيادة وقت الانتظار عند الخطأ
        
        if sent_any:
            sent_msg = bot.send_message(chat_id, "<b>تم الانتهاء من الإرسال بنجاح</b>", parse_mode="HTML")
            if chat_id not in user_messages:
                user_messages[chat_id] = []
            user_messages[chat_id].append(sent_msg.message_id)
        else:
            sent_msg = bot.send_message(chat_id, "<b>فشل جميع محاولات الإرسال</b>", parse_mode="HTML")
            if chat_id not in user_messages:
                user_messages[chat_id] = []
            user_messages[chat_id].append(sent_msg.message_id)
            
    except Exception as e:
        sent_msg = bot.send_message(chat_id, f"<b>خطأ أثناء عملية النشر: {str(e)}</b>", parse_mode="HTML")
        if chat_id not in user_messages:
            user_messages[chat_id] = []
        user_messages[chat_id].append(sent_msg.message_id)

# تشغيل البوت
if __name__ == "__main__":
    print("جارٍ تشغيل البوت...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"حدث خطأ: {e}")
        time.sleep(10)
        os.execv(__file__, sys.argv)