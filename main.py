import os
import random
import re
import time
import asyncio
import json
from telethon import TelegramClient, events
from telethon.tl.custom import Button 
from telethon.tl.types import User
from telethon.sessions import StringSession
from telethon.tl.functions.channels import InviteToChannelRequest, LeaveChannelRequest
from telethon.tl.types import InputPeerChannel
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest, GetParticipantRequest
from telethon.tl.types import InputPeerUser
from telethon.errors import AuthKeyError, SessionPasswordNeededError
from telethon.errors import UserAlreadyParticipantError, FloodWaitError



API_ID = int("26650843")
API_HASH = "6b9ebd8f67b08012b12c4132d45123b9"
DEVS = ["g9uuu", "DevVeGa", "TopVeGa"]
DEVS.append("DevVeGa")
bot_token = "8056680356:AAE-xK5thE2SmOOm5KkpcnYvh48ufZZFrCQ"

client = TelegramClient('bot_session', api_id=26650843, api_hash='6b9ebd8f67b08012b12c4132d45123b9')

from telethon import Button

@client.on(events.CallbackQuery(data=b'back_to_main'))
async def back_to_main_handler(event):
    try:
        buttons = [
            [Button.inline("🎯 حساب جديد", b"add_account"),
            Button.inline("🗑️ حذف حساب", b"remove_account")],
            [Button.inline("🧹 تنظيف الحسابات", b"safe_clean_scan"),
            Button.inline("📋 عرض الحسابات", b"show_accounts")],
            [Button.inline("🚫 الحسابات المحظورة", b"check_banned"),
            Button.inline("💣 مسح الكل", b"delete_all")],
            [Button.inline("🎁 فحص الجيفتات", b"check_banned")],
            [Button.inline("👍 رشق تفاعلات", b"check_banned"),
            Button.inline("👎 رشق تفاعلات", b"delete_all")],
            [Button.inline("📊 رشق استفتاء", b"check_banned"),
            Button.inline("🙈 رشق تفاعل محدد", b"delete_all")],
            [Button.inline("🚀 نقل الأعضاء", b"trans")],
            [Button.inline("📯 نقل بواسطه ملف", b"transss")],
            [Button.inline("🗃 تجميع في ملف", b"collect_members")],
            [Button.inline("➕ انضمام للجروب", b"invite_accounts"),
            Button.inline("👋 مغادرة جروب", b"leave_accounts")],
            [Button.inline("📤 رفع نسخة الجلسات", b"upload_sessions"),
            Button.inline("📂 جلب نسخة الجلسات", b"get_sessions")],
            [Button.inline("👋 مغادره كل الجروبات", b"leave_all"),
             Button.inline("⛔ إيقاف العمليات", "stop_operation")],
            [Button.inline("✅ جلب نسخه الاعضاء الناجحين", b"get_data")]
        ]
        await event.edit(
            "╮⦿ اهـلا بڪ عزيـزي المطـور الاساسـي │⎋ اليك كيب التحكم بالبوت",
            buttons=buttons
        )
        await event.answer()
    except Exception as e:
        await event.respond(
            "⚠️ حدث خطأ في عرض القائمة الرئيسية\n\n" + str(e),
            buttons=buttons
        )

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    if event.sender.username not in DEVS:
        return
    buttons = [
            [Button.inline("🎯 حساب جديد", b"add_account"),
            Button.inline("🗑️ حذف حساب", b"remove_account")],
            [Button.inline("🧹 تنظيف الحسابات", b"safe_clean_scan"),
            Button.inline("📋 عرض الحسابات", b"show_accounts")],
            [Button.inline("🚫 الحسابات المحظورة", b"check_banned"),
            Button.inline("💣 مسح الكل", b"delete_all")],
            [Button.inline("🎁 فحص الجيفتات", b"check_banned")],
            [Button.inline("👍 رشق تفاعلات", b"check_banned"),
            Button.inline("👎 رشق تفاعلات", b"delete_all")],
            [Button.inline("📊 رشق استفتاء", b"check_banned"),
            Button.inline("🙈 رشق تفاعل محدد", b"delete_all")],
            [Button.inline("🚀 نقل الأعضاء", b"trans")],
            [Button.inline("📯 نقل بواسطه ملف", b"transss")],
            [Button.inline("🗃 تجميع في ملف", b"collect_members")],
            [Button.inline("➕ انضمام للجروب", b"invite_accounts"),
            Button.inline("👋 مغادرة جروب", b"leave_accounts")],
            [Button.inline("📤 رفع نسخة الجلسات", b"upload_sessions"),
            Button.inline("📂 جلب نسخة الجلسات", b"get_sessions")],
            [Button.inline("👋 مغادره كل الجروبات", b"leave_all"),
             Button.inline("⛔ إيقاف العمليات", "stop_operation")],
            [Button.inline("✅ جلب نسخه الاعضاء الناجحين", b"get_data")]
    ]
    await event.respond("╮⦿ اهـلا بڪ عزيـزي المطـور الاساسـي │⎋ اليك كيب التحكم بالبوت", buttons=buttons)

@client.on(events.CallbackQuery(data=b'delete_all'))
async def delete_all_handler(event):
    try:
        if event.sender.username not in DEVS:
            await event.answer("⛔ ليس لديك صلاحيات لهذا الأمر!", alert=True)
            return

        await event.edit(
            "⚠️ **تحذير مهم!**\n\n"
            "هل أنت متأكد من حذف جميع الحسابات؟\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            "❌ هذا الإجراء لا يمكن التراجع عنه!\n",
            buttons=[
                [Button.inline("✅ تأكيد الحذف الكامل", b"confirm_delete_all")],
                [Button.inline("🔙 العودة للقائمة", b"back_to_main")]
            ]
        )
        
    except Exception as e:
        await event.answer(f"❌ حدث خطأ: {str(e)}", alert=True)

@client.on(events.CallbackQuery(data=b'confirm_delete_all'))
async def confirm_delete_all_handler(event):
    try:
        with open("accounts.json", "w", encoding='utf-8') as f:
            json.dump([], f)
        await event.edit(
            "✅ **تم الحذف بنجاح**\n\n",
            buttons=[
                [Button.inline("🔙 القائمة", b"back_to_main")]
            ]
        )
    except Exception as e:
        await event.edit(
            f"❌ فشل في الحذف: {str(e)}",
            buttons=[[Button.inline("🔙 العودة", b"back_to_main")]]
        )



@client.on(events.CallbackQuery(data=b'remove_account'))
async def remove_account(event):
    try:
        accounts = await load_accounts()
        if not accounts:
            await event.edit("❌ لا توجد حسابات مسجلة لحذفها!")
            return
        buttons = []
        for acc in accounts:
            acc_name = acc.get('name', 'غير معروف')
            acc_phone = acc.get('phone', 'غير معروف')
            btn_text = f"{acc_name} ({acc_phone})"
            buttons.append([Button.inline(btn_text, f"del_acc_{acc['phone']}")])
        buttons.append([Button.inline("❌ إلغاء", b"back_to_main")])
        await event.edit(
            "🗑️ **اختر الحساب الذي تريد حذفه:**",
            buttons=buttons
        )
    except Exception as e:
        await event.edit(f"❌ حدث خطأ أثناء تحضير قائمة الحسابات: {str(e)}")


@client.on(events.CallbackQuery(pattern=rb'del_acc_(.*)'))
async def confirm_delete(event):
    try:
        phone_to_delete = event.pattern_match.group(1).decode()
        accounts = await load_accounts()        
        account_to_delete = next((acc for acc in accounts if acc['phone'] == phone_to_delete), None)
        if not account_to_delete:
            await event.answer("❌ الحساب غير موجود!")
            return
        await event.edit(
            f"⚠️ **تأكيد الحذف**\n\n"
            f"هل أنت متأكد من حذف الحساب التالي؟\n\n"
            f"👤 الاسم: {account_to_delete.get('name', 'غير معروف')}\n"
            f"📞 الهاتف: {account_to_delete.get('phone', 'غير معروف')}\n"
            f"🔗 اليوزر: @{account_to_delete.get('username', 'غير معروف')}\n\n"
            "❗ لا يمكن التراجع عن هذه العملية",
            buttons=[
                [Button.inline("✅ نعم، احذف", f"confirm_del_{phone_to_delete}")],
                [Button.inline("❌ لا، إلغاء", b"remove_account")]
            ]
        )
    except Exception as e:
        await event.edit(f"❌ حدث خطأ أثناء تحضير تأكيد الحذف: {str(e)}")


@client.on(events.CallbackQuery(pattern=rb'confirm_del_(.*)'))
async def execute_delete(event):
    try:
        phone_to_delete = event.pattern_match.group(1).decode()
        accounts = await load_accounts()
        new_accounts = [acc for acc in accounts if acc['phone'] != phone_to_delete]
        
        if len(new_accounts) == len(accounts):
            await event.answer("❌ الحساب غير موجود!")
            return

        if await save_accounts(new_accounts):
            await event.edit(
                "✅ **تم حذف الحساب بنجاح!**",
                buttons=[Button.inline("🔙 العودة", b"back_to_main")]
            )
        else:
            await event.edit(
                "❌ فشل في حذف الحساب!",
                buttons=[Button.inline("🔙 العودة", b"back_to_main")]
            )
    except Exception as e:
        await event.edit(
            f"❌ حدث خطأ أثناء حذف الحساب: {str(e)}",
            buttons=[Button.inline("🔙 العودة", b"back_to_main")]
        )

BANNED_ACCOUNTS_CACHE = []

@client.on(events.CallbackQuery(data=b'check_banned'))
async def check_banned_handler(event):
    global BANNED_ACCOUNTS_CACHE
    try:
        if event.sender.username not in DEVS:
            await event.answer("❌ ليس لديك صلاحيات لهذا الأمر", alert=True)
            return
            
        try:
            progress_msg = await event.respond("🔄 جاري تحميل بيانات الحسابات...")
            with open("accounts.json", "r", encoding='utf-8') as f:
                accounts = json.load(f)
                
            if not accounts:
                await progress_msg.edit("❌ لا توجد حسابات مسجلة في قاعدة البيانات")
                return
        except Exception as e:
            await progress_msg.edit(f"❌ فشل تحميل ملف الحسابات: {str(e)}")
            return

        spam_bot = "SpamBot"
        BANNED_ACCOUNTS_CACHE = []
        banned_accounts = []
        active_accounts = []
        error_accounts = []
        total = len(accounts)
        processed = 0
        progress_report = await progress_msg.edit(f"""
🔄 **جاري فحص الحسابات**
━━━━━━━━━━━━━━━━
• الحسابات المفحوصة: 0/{total}
• النشطة: 0
• المحظورة: 0
• الأخطاء: 0
━━━━━━━━━━━━━━━━
⏳ المدة: 00:00:00
        """)
        start_time = time.time()
        for account in accounts:
            try:
                if processed % 5 == 0:
                    elapsed = int(time.time() - start_time)
                    elapsed_str = f"{elapsed//3600:02d}:{(elapsed%3600)//60:02d}:{elapsed%60:02d}"
                    await progress_report.edit(f"""
🔄 **جاري فحص الحسابات**
━━━━━━━━━━━━━━━━
• الحسابات المفحوصة: {processed}/{total}
• النشطة: {len(active_accounts)}
• المحظورة: {len(banned_accounts)}
• الأخطاء: {len(error_accounts)}
━━━━━━━━━━━━━━━━
⏳ المدة: {elapsed_str}
                    """)
                async with TelegramClient(
                    StringSession(account['session']),
                    API_ID,
                    API_HASH,
                    device_model="iPhone 13 Pro Max",
                    system_version="14.8",
                    app_version="8.4",
                    lang_code="ar",
                    timeout=10
                ) as user:
                    await user.start()
                    try:
                        await user.send_message(spam_bot, "/start")
                        await asyncio.sleep(1)
                        messages = []
                        async for msg in user.iter_messages(spam_bot, limit=1):
                            messages.append(msg.text.lower() if msg.text else "")
                            
                        if not messages:
                            active_accounts.append(account)
                        elif any(word in messages[0] for word in ["للأسف", "sorry", "محظور", "banned", "شرطه", "afraid"]):
                            banned_accounts.append(account)
                            BANNED_ACCOUNTS_CACHE.append(account)
                        else:
                            active_accounts.append(account)
                    except FloodWaitError as fwe:
                        continue
                    except Exception as e:
                        error_accounts.append((account, str(e)))
                processed += 1
            except Exception as e:
                error_accounts.append((account, f"خطأ في الجلسة: {str(e)}"))
                continue
        elapsed = int(time.time() - start_time)
        elapsed_str = f"{elapsed//3600:02d}:{(elapsed%3600)//60:02d}:{elapsed%60:02d}"
        report = f"""
📊 **نتائج فحص الحسابات**
━━━━━━━━━━━━━━━━
• ✅ الحسابات النشطة: {len(active_accounts)}
• ⛔ الحسابات المحظورة: {len(banned_accounts)}
• ⚠️ الحسابات التي بها أخطاء: {len(error_accounts)}
• ⏳ المدة المستغرقة: {elapsed_str}
━━━━━━━━━━━━━━━━
        """
        if banned_accounts:
            report += "\n🔴 **الحسابات المحظورة:**\n"
            for acc in banned_accounts[:5]:
                name = acc.get('name', 'غير معروف')
                phone = acc.get('phone', 'لا يوجد رقم')
                username = f"@{acc.get('username')}" if acc.get('username') else "لا يوجد يوزر"
                report += f"├─ {name} - {phone} - {username}\n"
            if len(banned_accounts) > 5:
                report += f"└─ و {len(banned_accounts)-5} حساب آخر\n"
        if error_accounts:
            report += "\n🟠 **أهم الأخطاء:**\n"
            for acc, error in error_accounts[:3]:
                name = acc.get('name', 'غير معروف')
                report += f"├─ {name}: {error[:60]}{'...' if len(error)>60 else ''}\n"
            if len(error_accounts) > 3:
                report += f"└─ و {len(error_accounts)-3} خطأ آخر\n"
        await progress_msg.delete()
        result_msg = await event.respond(report)
        if banned_accounts:
            await result_msg.reply(
                "هل تريد حذف الحسابات المحظورة؟",
                buttons=[
                    [Button.inline("🗑️ حذف الحسابات المحظورة", b"delete_banned")],
                    [Button.inline("📋 تصدير القائمة", b"export_banned")],
                    [Button.inline("🔙 الرجوع للقائمة", b"back_to_main")]
                ]
            )
        else:
            await result_msg.reply(
                "✅ لا توجد حسابات محظورة",
                buttons=[[Button.inline("🔙 الرجوع للقائمة", b"back_to_main")]]
            )
    except Exception as e:
        await event.respond(f"❌ حدث خطأ جسيم أثناء الفحص:\n{str(e)}")


@client.on(events.CallbackQuery(data=b'delete_banned'))
async def delete_banned_handler(event):
    try:
        original_msg = await event.get_message()
        banned_section = original_msg.text.split("الحسابات المحظورة:")[-1].split("\n\n")[0]
        banned_count = banned_section.count("├─")  
        if banned_count == 0:
            banned_count = len(re.findall(r"الحسابات المحظورة: (\d+)", original_msg.text))
            if banned_count == 0:
                banned_count = original_msg.text.count("محظور")
        await event.edit(
            f"⚠️ **تأكيد الحذف**\n\n"
            f"أنت على وشك حذف {banned_count} حساب محظور\n"
            f"❗ لا يمكن التراجع عن هذه العملية\n\n"
            "هل أنت متأكد من المتابعة؟",
            buttons=[
                [Button.inline("✅ نعم، احذف الكل", b"confirm_delete_banned")],
                [Button.inline("🔍 معاينة الحسابات", b"preview_banned")],
                [Button.inline("❌ إلغاء", b"cancel_delete_banned")]
            ]
        )
    except Exception as e:
        await event.respond(
            "❌ حدث خطأ أثناء تحضير خيارات الحذف\n"
            "يرجى المحاولة مرة أخرى أو مراجعة السجلات",
            buttons=[[Button.inline("🔙 الرجوع", b"back_to_main")]]
        )

@client.on(events.CallbackQuery(data=b'preview_banned'))
async def preview_banned_handler(event):
    try:
        original_msg = await event.get_message()
        banned_section = original_msg.text.split("الحسابات المحظورة:")[1].split("\n\n")[0]
        await event.edit(
            f"🔍 **معاينة الحسابات المحظورة**\n\n"
            f"{banned_section}\n\n"
            "هل تريد متابعة الحذف؟",
            buttons=[
                [Button.inline("✅ نعم، احذف الكل", b"confirm_delete_banned")],
                [Button.inline("❌ إلغاء", b"cancel_delete_banned")]
            ]
        )
    except Exception as e:
        await event.respond(f"❌ خطأ في عرض المعاينة: {str(e)}")


@client.on(events.CallbackQuery(data=b'confirm_delete_banned'))
async def confirm_delete_banned_handler(event):
    global BANNED_ACCOUNTS_CACHE
    try:
        if not BANNED_ACCOUNTS_CACHE:
            await event.answer("⚠️ لا توجد حسابات محظورة في الذاكرة المؤقتة", alert=True)
            return
        progress_msg = await event.respond("🔄 جاري حذف الحسابات المحظورة...")
        with open("accounts.json", "r", encoding='utf-8') as f:
            accounts = json.load(f)
        banned_phones = {acc.get('phone') for acc in BANNED_ACCOUNTS_CACHE}
        valid_accounts = [acc for acc in accounts if acc.get('phone') not in banned_phones]
        with open("accounts.json", "w", encoding='utf-8') as f:
            json.dump(valid_accounts, f, ensure_ascii=False, indent=2)
        banned_count = len(BANNED_ACCOUNTS_CACHE)
        BANNED_ACCOUNTS_CACHE = []
        await progress_msg.delete()
        await event.respond(
            f"✅ تم الانتهاء من عملية الحذف\n\n"
            f"🗑️ عدد الحسابات المحذوفة: {banned_count}\n"
            f"📊 الحسابات المتبقية: {len(valid_accounts)}",
            buttons=[[Button.inline("🔙 الرجوع للقائمة", b"back_to_main")]]
        )
    except Exception as e:
        await event.respond(
            f"❌ فشل في حذف الحسابات المحظورة:\n{str(e)}",
            buttons=[[Button.inline("🔙 الرجوع للقائمة", b"back_to_main")]]
        )

@client.on(events.CallbackQuery(data=b'cancel_delete_banned'))
async def cancel_delete_banned_handler(event):
    await event.answer("❌ تم إلغاء عملية الحذف")
    await event.delete()

async def validate_session(session_str):
    temp_client = None
    try:
        temp_client = TelegramClient(
            StringSession(session_str),
            API_ID,
            API_HASH,
            timeout=15
        )
        
        await temp_client.connect()
        if not await temp_client.is_user_authorized():
            return "invalid"        
        try:
            me = await temp_client.get_me()
            if not me:
                return "invalid"
            return "valid"
            
        except Exception as inner_e:
            return f"invalid: {str(inner_e)}"
            
    except Exception as e:
        error_msg = str(e)
        if "Please enter your phone" in error_msg:
            return "invalid: not authorized"
        elif "AUTH_KEY_DUPLICATED" in error_msg:
            return "invalid: duplicated"
        elif "TimeoutError" in error_msg:
            return "timeout"
        elif "Cannot connect to host" in error_msg:
            return "error: connection failed"
        else:
            return f"error: {error_msg}"
            
    finally:
        if temp_client:
            try:
                await temp_client.disconnect()
            except Exception as disc_e:
                pass

@client.on(events.CallbackQuery(data=b'safe_clean_scan'))
async def clean_accounts_safely(event, delete_invalid=False):
    try:
        accounts = await load_accounts()
        valid_accounts = []
        invalid_accounts = []
        progress_msg = await event.respond("🔄 بدء الفحص الآمن للجلسات...")
        
        if not delete_invalid:
            event.client.invalid_accounts_cache = []
            for index, account in enumerate(accounts):
                try:
                    status = await asyncio.wait_for(
                        validate_session(account['session']),
                        timeout=15
                    )
                    if status == "valid":
                        valid_accounts.append(account)
                    else:
                        invalid_accounts.append(account)
                        event.client.invalid_accounts_cache.append(account)
                except asyncio.TimeoutError:
                    invalid_accounts.append(account)
                    event.client.invalid_accounts_cache.append(account)
                except Exception as e:
                    invalid_accounts.append(account)
                    event.client.invalid_accounts_cache.append(account)
            
                if index % 10 == 0 or index == len(accounts) - 1:
                    await progress_msg.edit(
                        f"🔍 جاري الفحص ({index+1}/{len(accounts)})\n"
                        f"✅ الصالحة: {len(valid_accounts)}\n"
                        f"❌ غير الصالحة: {len(invalid_accounts)}"
                    )
                await asyncio.sleep(0.5)
        if delete_invalid:
            valid_accounts = [acc for acc in accounts if acc not in event.client.invalid_accounts_cache]
            await save_accounts(valid_accounts)
            
            deleted_list = "\n".join([f"• {acc.get('phone', 'Unknown')} ({acc.get('session_name', 'No name')})" 
                                     for acc in event.client.invalid_accounts_cache])
            
            result_text = (
                f"🧹 **تم حذف الحسابات غير الصالحة**\n\n"
                f"• الحسابات المفحوصة: {len(accounts)}\n"
                f"• الحسابات الصالحة: {len(valid_accounts)}\n"
                f"• الحسابات المحذوفة: {len(event.client.invalid_accounts_cache)}\n\n"
                f"**قائمة الحسابات المحذوفة:**\n"
                f"{deleted_list}"
            )
            buttons = [
                [Button.inline("🔙 القائمة الرئيسية", b"back_to_main")]
            ]
        else:
            result_text = (
                f"📊 **نتائج الفحص**\n\n"
                f"• الحسابات المفحوصة: {len(accounts)}\n"
                f"• الحسابات الصالحة: {len(valid_accounts)}\n"
                f"• الحسابات غير الصالحة: {len(invalid_accounts)}\n\n"
            )
            
            if invalid_accounts:
                sample_list = "\n".join([f"• {acc.get('phone', 'Unknown')} ({acc.get('session_name', 'No name')})" 
                                       for acc in invalid_accounts[:5]])
                result_text += (
                    f"**عينة من الحسابات غير الصالحة:**\n"
                    f"{sample_list}\n"
                )
                if len(invalid_accounts) > 5:
                    result_text += f"و {len(invalid_accounts)-5} أخرى...\n\n"
                result_text += "هل تريد حذف الحسابات غير الصالحة؟"
                buttons = [
                    [Button.inline("🗑️ حذف غير الصالحة", b"confirm_delete_invalid")],
                    [Button.inline("🔙 الاحتفاظ بها", b"back_to_main")]
                ]
            else:
                result_text += "لا توجد حسابات غير صالحة للحذف"
                buttons = [
                    [Button.inline("🔙 القائمة الرئيسية", b"back_to_main")]
                ]
        
        await progress_msg.edit(
            result_text,
            buttons=buttons
        )
    except Exception as e:
        await event.respond(
            f"⚠️ حدث خطأ في العملية الرئيسية\n{str(e)}",
            buttons=[[Button.inline("🔙 العودة", b"back_to_main")]]
        )


@client.on(events.CallbackQuery(data=b'confirm_delete_invalid'))
async def confirm_delete_invalid(event):
    await clean_accounts_safely(event, delete_invalid=True)


stop_event = asyncio.Event()

@client.on(events.CallbackQuery(data=b'stop_operation'))
async def stop_handler(event):
    stop_event.set()
    await event.answer("⏹ تم إيقاف العملية بنجاح")



@client.on(events.CallbackQuery(data=b'invite_accounts'))
async def invite_accounts_handler(event):
    try:
        async with client.conversation(event.chat_id) as conv:
            await conv.send_message("🔗 أرسل رابط الجروب (مثال: @mygroup أو t.me/mygroup)")
            group_response = await conv.get_response()
            group_link = group_response.text.strip()
            if "https://" in group_link and "+" not in group_link:
                group_username = group_link.replace("https://t.me/", "")
            else:
                group_username = group_link.replace("@", "")
            await event.answer("🔄 جاري دعوة الحسابات للجروب...")
            accounts = await load_accounts()
            if not accounts:
                await event.answer("❌ لا توجد حسابات مسجلة")
                return
            success = 0
            failed = 0
            for account in accounts:
                try:
                    async with TelegramClient(
                        StringSession(account['session']),
                        API_ID,
                        API_HASH
                    ) as user:
                        await user.start()
                        try:
                            await user(JoinChannelRequest(group_username))
                            success += 1
                        except Exception as e:
                            failed += 1
                        await asyncio.sleep(1)
                except Exception as e:
                    failed += 1
            await event.answer(
                f"✅ تمت العملية بنجاح\n\n"
                f"• انضم {success} حساب\n"
                f"• فشل {failed} حساب",
                alert=True
            )
            await event.edit(
                "تم تنفيذ الأمر بنجاح",
                buttons=[[Button.inline("🔙 عودة", "back_to_main")]]
            )
    except Exception as e:
        await event.answer(f"❌ حدث خطأ: {str(e)}", alert=True)

@client.on(events.CallbackQuery(data=b'leave_accounts'))
async def leave_accounts_handler(event):
    try:
        async with client.conversation(event.chat_id) as conv:
            await conv.send_message("🔗 أرسل رابط الجروب (مثال: @mygroup أو t.me/mygroup)")
            group_response = await conv.get_response()
            group_link = group_response.text.strip()
            if "https://" in group_link and "+" not in group_link:
                group_username = group_link.replace("https://t.me/", "")
            else:
                group_username = group_link.replace("@", "")
            await event.answer("🔄 جاري مغادرة الحسابات من الجروب...")
            accounts = await load_accounts()
            if not accounts:
                await event.answer("❌ لا توجد حسابات مسجلة")
                return
            success = 0
            failed = 0
            for account in accounts:
                try:
                    async with TelegramClient(
                        StringSession(account['session']),
                        API_ID,
                        API_HASH
                    ) as user:
                        await user.start()
                        try:
                            await user(LeaveChannelRequest(
                                await user.get_entity(group_username)
                            ))
                            success += 1
                        except Exception as e:
                            failed += 1
                        await asyncio.sleep(1)
                except Exception as e:
                    failed += 1
            await event.answer(
                f"✅ تمت العملية بنجاح\n\n"
                f"• غادر {success} حساب\n"
                f"• فشل {failed} حساب",
                alert=True
            )
            await event.edit(
                "تم تنفيذ الأمر بنجاح",
                buttons=[[Button.inline("🔙 عودة", "back_to_main")]]
            )
    except Exception as e:
        await event.answer(f"❌ حدث خطأ: {str(e)}", alert=True)
    
@client.on(events.CallbackQuery(data=b'get_sessions'))
async def get_sessions_handler(event):
    if event.sender.username not in DEVS:
        return    
    if not os.path.exists("accounts.json"):
        await event.answer("❌ لا يوجد ملف جلسات")
        return
    try:
        await client.send_file(
            event.chat_id,
            "accounts.json",
            caption="📂 النسخة الاحتياطية للجلسات",
            force_document=True
        )
        await event.answer()
    except Exception as e:
        await event.answer(f"❌ خطأ في إرسال الملف: {str(e)}")

@client.on(events.CallbackQuery(data=b'get_data'))
async def get_data_handler(event):
    if event.sender.username not in DEVS:
        return    
    if not os.path.exists("data.txt"):
        await event.answer("❌ لا يوجد ملف جلسات")
        return
    try:
        await client.send_file(
            event.chat_id,
            "data.txt",
            caption="📂 النسخة الاحتياطية لليوزرات",
            force_document=True
        )
        await event.answer()
    except Exception as e:
        await event.answer(f"❌ خطأ في إرسال الملف: {str(e)}")
@client.on(events.CallbackQuery(data=b'get_sessions'))
async def get_sessions_handler(event):
    if event.sender.username not in DEVS:
        return    
    if not os.path.exists("accounts.json"):
        await event.answer("❌ لا يوجد ملف جلسات")
        return
    try:
        await client.send_file(
            event.chat_id,
            "accounts.json",
            caption="📂 النسخة الاحتياطية للجلسات",
            force_document=True
        )
        await event.answer()
    except Exception as e:
        await event.answer(f"❌ خطأ في إرسال الملف: {str(e)}")

@client.on(events.CallbackQuery(data=b'upload_sessions'))
async def upload_sessions_handler(event):
    if event.sender.username not in DEVS:
        return
    async with client.conversation(event.chat_id) as conv:
        await conv.send_message("📤 يرجى إرسال ملف الجلسات (accounts.json)")
        try:
            file_msg = await conv.get_response()
            if file_msg.file:
                file_path = await file_msg.download_media(file="accounts.json")
                await event.answer("✅ تم تحديث الجلسات بنجاح")
            else:
                await event.answer("❌ لم يتم إرسال ملف صحيح")
        except Exception as e:
            await event.answer(f"❌ خطأ في التحديث: {str(e)}")

@client.on(events.CallbackQuery(pattern=rb'page_(show|remove)_(\d+)'))
async def handle_pagination(event):
    action = event.pattern_match.group(1).decode()
    page = int(event.pattern_match.group(2))
    await show_accounts(event, page, action)

@client.on(events.CallbackQuery(data=b'show_accounts'))
async def show_accounts_handler(event):
    await show_accounts(event)

@client.on(events.CallbackQuery(data=b'remove_accounts'))
async def remove_accounts_handler(event):
    await show_accounts(event, action="remove")

ACCOUNTS_FILE = "accounts.json"

async def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return []
    
    try:
        with open(ACCOUNTS_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading accounts: {e}")
        return []

async def save_accounts(accounts):
    try:
        with open(ACCOUNTS_FILE, "w", encoding='utf-8') as f:
            json.dump(accounts, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving accounts: {e}")
        return False

async def load_sessions():
    try:
        if not os.path.exists("accounts.json"):
            return []
        with open("accounts.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            return [account["session"] for account in data if "session" in account]
    except Exception as e:
        print(f"Error loading sessions: {e}")
        return None
    
@client.on(events.CallbackQuery(data=b'add_account'))
async def add_account(event):
    try:
        async with client.conversation(event.chat_id, timeout=300) as conv:
            await conv.send_message(
                "📝 **إضافة حساب جديد**\n\n"
                "يرجى إرسال جلسة الحساب (كود الجلسة)\n\n"
                "▪ تأكد من صحة الجلسة\n"
                "▪ لا تشارك هذا الكود مع أحد\n"
                "▪ للإلغاء اكتب /cancel\n\n"
                "⏳ لديك 5 دقائق لإتمام العملية",
                buttons=Button.force_reply()
            )
            session_response = await conv.get_response()
            if session_response.text.strip() == "/cancel":
                await session_response.reply("❌ تم إلغاء العملية")
                return
            session = session_response.text.strip()
            if not session or len(session) < 50:
                await conv.send_message("⚠️ الجلسة غير صالحة! يجب أن يكون طول الجلسة أكثر من 50 حرفاً")
                return
            accounts = await load_accounts()
            if any(acc['session'] == session for acc in accounts):
                await conv.send_message("⚠️ هذه الجلسة مضافة مسبقاً!")
                return
            temp_client = TelegramClient(StringSession(session), API_ID, API_HASH)
            try:
                await temp_client.start()
                me = await temp_client.get_me()
                account_info = {
                    "name": f"{me.first_name or ''} {me.last_name or ''}".strip(),
                    "username": me.username or "",
                    "phone": me.phone or "",
                    "session": session
                }
                accounts.append(account_info)
                if await save_accounts(accounts):
                    await conv.send_message(
                        f"✅ **تمت إضافة الحساب بنجاح!**\n\n"
                        f"👤 الاسم: {account_info['name']}\n"
                        f"📞 الهاتف: {account_info['phone']}\n"
                        f"🔗 اليوزر: @{account_info['username']}\n\n"
                        "تم حفظ الجلسة وتفعيلها بنجاح.",
                        buttons=Button.clear()
                    )
                else:
                    await conv.send_message("❌ فشل في حفظ الحساب!")
            except Exception as e:
                await conv.send_message(f"❌ فشل في تفعيل الجلسة: {str(e)}")
            finally:
                await temp_client.disconnect()
    except asyncio.TimeoutError:
        await event.respond("⌛ انتهى الوقت المحدد لإدخال الجلسة")
    except Exception as e:
        await event.respond(f"❌ حدث خطأ غير متوقع: {str(e)}")

async def show_accounts(event, current_page=0, action="show"):
    try:
        accounts = await load_accounts()
        if not accounts:
            return await event.edit("❌ لا توجد حسابات مضافة حالياً.")
        accounts_per_page = 8
        total_pages = (len(accounts) + accounts_per_page - 1) // accounts_per_page
        current_page = max(0, min(current_page, total_pages - 1))
        start_idx = current_page * accounts_per_page
        page_accounts = accounts[start_idx:start_idx + accounts_per_page]
        buttons = []
        for idx, acc in enumerate(page_accounts, start=start_idx + 1):
            display_name = (
                acc.get('name') or 
                f"@{acc['username']}" if acc.get('username') else 
                f"الحساب رقم {idx}"
            )
            if action == "remove":
                buttons.append([Button.inline(f"❌ {display_name}", f"del_{accounts.index(acc)}")])
            else:
                buttons.append([Button.inline(f"👤 {display_name}", "no_action")])
        nav_buttons = []
        if current_page > 0:
            nav_buttons.append(Button.inline("◀️ السابق", f"page_{action}_{current_page-1}"))
        if current_page < total_pages - 1:
            nav_buttons.append(Button.inline("التالي ▶️", f"page_{action}_{current_page+1}"))
        if nav_buttons:
            buttons.append(nav_buttons)
        buttons.append([Button.inline("🔙 رجوع", "back_to_main")])
        await event.edit(
            f"📋 **قائمة الحسابات**\n"
            f"• العدد الإجمالي: {len(accounts)}\n"
            f"• الصفحة: {current_page + 1}/{total_pages}\n\n"
            f"{'⬇️ اختر حسابًا للحذف:' if action == 'remove' else '⬇️ الحسابات المضافة:'}",
            buttons=buttons
        )
    except Exception as e:
        await event.edit(f"❌ حدث خطأ: {str(e)}")

@client.on(events.CallbackQuery(pattern=rb'del_(\d+)'))
async def delete_account(event):
    acc_index = int(event.pattern_match.group(1))
    accounts = await load_accounts()
    
    if 0 <= acc_index < len(accounts):
        deleted_acc = accounts.pop(acc_index)
        if await save_accounts(accounts):
            await event.answer(f"✅ تم حذف الحساب: {deleted_acc.get('name', 'حساب بدون اسم')}")
            await show_accounts(event, action="remove")
        else:
            await event.answer("❌ فشل في حفظ التغييرات!")
    else:
        await event.answer("❌ رقم الحساب غير صحيح!")


from telethon.tl.types import ChannelParticipantsRecent, ChannelParticipantsSearch
from telethon.errors import UserAlreadyParticipantError, UserPrivacyRestrictedError, FloodWaitError


from telethon.tl.types import ChannelParticipantsRecent, ChannelParticipantsSearch
from telethon.errors import UserAlreadyParticipantError, UserPrivacyRestrictedError, FloodWaitError
from telethon.tl.functions.channels import GetParticipantRequest, JoinChannelRequest, InviteToChannelRequest
from telethon.tl.types import InputPeerUser

from telethon import TelegramClient, events
from telethon.tl.functions.channels import (
    JoinChannelRequest,
    GetParticipantRequest,
    InviteToChannelRequest
)
from telethon.tl.types import (
    InputPeerUser,
    ChannelParticipant,
    ChannelParticipantsSearch
)
from telethon.errors import (
    FloodWaitError,
    UserAlreadyParticipantError,
    UserPrivacyRestrictedError,
    ChannelPrivateError,
    UserNotMutualContactError
)
from telethon.sessions import StringSession
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest, GetParticipantRequest
from telethon.tl.types import InputPeerUser
from telethon.errors import UserAlreadyParticipantError, FloodWaitError
import asyncio
import time


from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest, GetParticipantRequest
from telethon.tl.types import InputPeerUser
from telethon.errors import UserAlreadyParticipantError, FloodWaitError
import asyncio
import time


@client.on(events.CallbackQuery(data=b'trans'))
async def trans_handler(event):
    try:
        stop_event.clear()
        async with client.conversation(event.chat_id, timeout=300) as conv:
            await conv.send_message("🔢 **الرجاء إدخال عدد الأعضاء المراد نقلهم:**\n(مثال: 50)")
            number_response = await conv.get_response()
            number = min(int(number_response.text.strip()), 20000)
            
            await conv.send_message("📥 **الرجاء إدخال رابط المجموعة المصدر:**\n(مثال: @SUPP_MATRIX أو https://t.me/SUPP_MATRIX)")
            source_response = await conv.get_response()
            source_chat = source_response.text.replace("@", "").replace("https://t.me/", "").strip()
            
            await conv.send_message("📤 **الرجاء إدخال رابط المجموعة الهدف:**\n(مثال: @sghiiuyggh أو https://t.me/sghiiuyggh)")
            target_response = await conv.get_response()
            target_chat = target_response.text.replace("@", "").replace("https://t.me/", "").strip()
        processing_msg = await event.edit("🔄 جاري بدء العملية...")

        max_per_acc = 49
        count = 0
        failed_users = set()
        added_users = set()
        skipped_users = set()

        sessions = await load_sessions()

        if not sessions:
            await event.edit("❌ لا توجد جلسات في ملف sessions.txt")
            return

        start_time = time.time()
        processed_accounts = 0

        for session_str in sessions:

            if stop_event.is_set():
                break
            
            if count >= number:
                break

            user = TelegramClient(StringSession(session_str), API_ID, API_HASH)
            processed_accounts += 1
            
            try:
                await user.start()
                me = await user.get_me()
                account_name = f"@{me.username}" if me.username else f"user_id:{me.id}"
                print(f"🔹 بدأت جلسة للحساب: {account_name}")

                try:
                    source_entity = await user.get_entity(source_chat)
                    target_entity = await user.get_entity(target_chat)
                except Exception as e:
                    print(f"❌ خطأ في الحصول على الكيانات: {str(e)}")
                    continue

                try:
                    await user(JoinChannelRequest(source_entity))
                    print(f"   ✅ انضم إلى المصدر: {source_chat}")
                except UserAlreadyParticipantError:
                    print(f"   ℹ️ الحساب موجود بالفعل في المصدر")
                except Exception as e:
                    print(f"   ❌ خطأ في الانضمام للمصدر: {str(e)}")
                    continue

                try:
                    await user(JoinChannelRequest(target_entity))
                    print(f"   ✅ انضم إلى الهدف: {target_chat}")
                except UserAlreadyParticipantError:
                    print(f"   ℹ️ الحساب موجود بالفعل في الهدف")
                except Exception as e:
                    print(f"   ❌ خطأ في الانضمام للهدف: {str(e)}")
                    continue

                await asyncio.sleep(2)

                try:
                    current_account_added = 0
                    
                    async for member in user.iter_participants(source_entity, aggressive=True):
                        if count >= number or current_account_added >= max_per_acc:
                            break
                        
                        if stop_event.is_set():
                            break

                        if member.bot or member.deleted:
                            continue

                        if member.id in added_users or member.id in skipped_users:
                            continue

                        if member.id in failed_users:
                            continue

                        try:
                            await user(GetParticipantRequest(target_entity, member))
                            skipped_users.add(member.id)
                            print(f"   ⏩ تخطي عضو موجود: {member.id}")
                            continue
                        except:
                            pass

                        try:
                            await user(InviteToChannelRequest(
                                target_entity,
                                [InputPeerUser(member.id, member.access_hash)]
                            ))
                            
                            await asyncio.sleep(2)
                            try:
                                participant = await user(GetParticipantRequest(target_entity, member))
                                if participant and hasattr(participant, 'participant'):
                                    added_users.add(member.id)
                                    count += 1
                                    current_account_added += 1
                                    print(f"   ✅ تمت إضافة عضو بنجاح: {member.id}")
                                else:
                                    failed_users.add(member.id)
                                    print(f"   ❌ لم يتم العثور على العضو بعد الإضافة: {member.id}")
                            except Exception as e:
                                failed_users.add(member.id)
                                print(f"   ❌ فشل التحقق من العضو المضاف: {member.id} - {str(e)}")
                            
                            delay = max(2, min(10, 60 / max_per_acc))
                            await asyncio.sleep(1)
                            
                        except UserAlreadyParticipantError:
                            skipped_users.add(member.id)
                            print(f"   ⏩ تخطي عضو موجود: {member.id}")
                        except FloodWaitError as fwe:
                            break
                        except Exception as e:
                            failed_users.add(member.id)
                            print(f"   ❌ فشل إضافة عضو {member.id}: {str(e)}")
                            await asyncio.sleep(5)

                except Exception as e:
                    print(f"❌ خطأ في جلب الأعضاء: {str(e)}")
                
                try:
                    await client.send_message(
                        event.chat_id,
                        f"📊 **تقرير الحساب {account_name}**\n"
                        f"✅ تمت إضافة: {current_account_added} عضو\n"
                        f"⏩ تم تخطي: {len([m for m in skipped_users if m not in added_users])} عضو (موجودين مسبقاً)\n"
                        f"❌ فشل في إضافة: {len([m for m in failed_users if m not in skipped_users])} عضو\n"
                        f"🔢 الإجمالي حتى الآن: {count}/{number}"
                    )
                except Exception as e:
                    print(f"❌ فشل إرسال تقرير الحساب: {str(e)}")

            except Exception as e:
                print(f"❌ خطأ عام في الجلسة: {str(e)}")
            finally:
                try:
                    await user.disconnect()
                except:
                    pass

        elapsed_time = int(time.time() - start_time)
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        result_message = (
            f"🎉 **النتائج النهائية**\n\n"
            f"⏱️ المدة: {time_str}\n"
            f"🔢 العدد المستهدف: {number} عضو\n"
            f"✅ تمت إضافة: {count} عضو\n"
            f"⏩ تم تخطي: {len(skipped_users)} عضو (موجودين مسبقاً)\n"
            f"❌ فشل في إضافة: {len(failed_users)} عضو\n"
            f"👥 عدد الحسابات المستخدمة: {processed_accounts}\n\n"
            f"📌 المصدر: {source_chat}\n"
            f"🎯 الهدف: {target_chat}"
        )

        try:
            await client.send_message(
                event.chat_id,
                result_message,
                buttons=[Button.inline("🔙 العودة", b"back_to_main")]
            )
            await processing_msg.delete()
        except Exception as e:
            print(f"❌ فشل إرسال التقرير النهائي: {str(e)}")
            await processing_msg.edit(
                result_message,
                buttons=[Button.inline("🔙 العودة", b"back_to_main")]
            )

    except Exception as e:
        error_msg = f"❌ حدث خطأ غير متوقع:\n{str(e)}"
        try:
            await client.send_message(
                event.chat_id,
                error_msg,
                buttons=[Button.inline("🔙 العودة", b"back_to_main")]
            )
        except:
            await event.edit(
                error_msg,
                buttons=[Button.inline("🔙 العودة", b"back_to_main")]
            )


from telethon.tl.types import DocumentAttributeFilename
import random
from telethon.tl.types import (
    UserStatusRecently,  # النشطين (آخر 24 ساعة)
    UserStatusLastWeek,  # شبه النشطين (آخر أسبوع)
    UserStatusLastMonth, # غير النشطين (أكثر من شهر)
    UserStatusOffline    # غير متصلين منذ فترة طويلة
)


@client.on(events.CallbackQuery(data=b'collect_members'))
async def collect_members_handler(event):
    try:
        await event.edit(
            "🔍 اختر نوع الأعضاء الذين تريد جمعهم:",
            buttons=[
                [Button.inline("🙈 تجميع مخفي", b'collect_active_members')],
                [Button.inline("✅ النشطين (آخر 24 ساعة)", b'filter_recent')],
                [Button.inline("🟢 شبه النشطين (آخر أسبوع)", b'filter_week')],
                [Button.inline("🟡 غير النشطين (أكثر من شهر)", b'filter_month')],
                [Button.inline("🔴 غير النشطين منذ مده", b'filter_verified')],
                [Button.inline("🌟 جميع الأعضاء", b'filter_all')]
            ]
        )
    except Exception as e:
        await event.edit(f"❌ حدث خطأ: {str(e)}")

@client.on(events.CallbackQuery(pattern=rb'filter_(verified|recent|week|month|all)'))
async def filter_selection_handler(event):
    try:
        filter_type = event.pattern_match.group(1).decode()
        await event.answer(f"تم اختيار: {filter_type}")
        session = await load_sessions()
        session_str = session[0]
        async with client.conversation(event.chat_id) as conv:
            await conv.send_message("📥 الرجاء إرسال يوزر المجموعة المصدر وضع علامه @:")
            source_response = await conv.get_response()
            source_chat = source_response.text.replace("@", "").strip()
            await conv.send_message("🔢 العدد الأقصى (حتى 10,000):")
            limit_response = await conv.get_response()
            try:
                max_members = min(int(limit_response.text), 100000)
            except:
                max_members = 100000
        user_client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
        await user_client.start()
        processing_msg = await event.edit("🔄 جاري جمع الأعضاء...")
        try:
            source_entity = await user_client.get_entity(source_chat)
            filename = f"members_{source_chat}_{filter_type}.txt"
            try:
                await user_client(JoinChannelRequest(source_entity))
            except Exception as e:
                print(f"⚠️ {e}")
            members_count = 0
            with open(filename, 'w', encoding='utf-8') as f:
                async for member in user_client.iter_participants(source_entity, limit=max_members):
                    if member.bot:
                        continue                        
                    if filter_type == 'verified' and not isinstance(member.status, UserStatusOffline):
                        continue
                    elif filter_type == 'recent' and not isinstance(member.status, UserStatusRecently):
                        continue
                    elif filter_type == 'week' and not isinstance(member.status, (UserStatusRecently, UserStatusLastWeek)):
                        continue
                    elif filter_type == 'month' and not isinstance(member.status, UserStatusLastMonth):
                        continue
                    if member.username:
                        f.write(f"{member.username}\n")
                        members_count += 1
                        if members_count % 50 == 0:
                            await processing_msg.edit(
                                f"🔄 تم جمع {members_count} عضو\n"
                                f"🔍 الفلتر: {filter_type}"
                            )
            buttons = [
                [Button.inline("📥 تحميل الملف", data=f'download_{filename}')],
                [Button.inline("🔙 عودة", b'back')]
            ]
            await event.edit(
                f"✅ تم الانتهاء!\n"
                f"📊 العدد: {members_count}\n"
                f"💾 الملف: {filename}",
                buttons=buttons
            )
        except Exception as e:
            await event.edit(f"❌ خطأ في الجمع: {str(e)}")
        finally:
            await user_client.disconnect()
    except Exception as e:
        await event.edit(f"❌ حدث خطأ: {str(e)}")

from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.messages import DeleteChatUserRequest

@client.on(events.CallbackQuery(pattern=rb'leave_all'))
async def leave_all_handler(event):
    try:
        accounts = await load_accounts()
        if not accounts:
            await event.edit("❌ لا توجد حسابات مسجلة!")
            return
        buttons = []
        for acc in accounts:
            acc_name = acc.get('name', 'غير معروف')
            acc_phone = acc.get('phone', 'غير معروف')
            btn_text = f"{acc_name} ({acc_phone})"
            buttons.append([Button.inline(btn_text, f"select_acc:{acc['phone']}".encode())])
        buttons.append([Button.inline('✅ كل الحسابات', b'select_acc:all')])
        buttons.append([Button.inline('❌ إلغاء', b'cancel_leave')])
        await event.edit(
            '⚠️ **اختر الحسابات التي تريد مغادرة المجموعات منها:**\n'
            'سيتم مغادرة جميع المجموعات والقنوات للحساب المحدد!',
            buttons=buttons
        )
    except Exception as e:
        await event.respond(f'حدث خطأ: {str(e)}')

@client.on(events.CallbackQuery(pattern=rb'select_acc:(.*)'))
async def select_account(event):
    try:
        selected_phone = event.pattern_match.group(1).decode()
        accounts = await load_accounts()
        if selected_phone == 'all':
            buttons = [
                [Button.inline('✅ تأكيد مغادرة الكل', b'confirm_leave:all')],
                [Button.inline('❌ إلغاء', b'cancel_leave')]
            ]
            await event.edit(
                '⚠️ **هل أنت متأكد من مغادرة جميع المجموعات لكل الحسابات؟**\n'
                'هذه العملية لا يمكن التراجع عنها!',
                buttons=buttons
            )
        else:
            selected_acc = next((acc for acc in accounts if acc['phone'] == selected_phone), None)
            if not selected_acc:
                await event.edit("❌ الحساب المحدد غير موجود!")
                return
            buttons = [
                [Button.inline(f'✅ تأكيد مغادرة {selected_acc["name"]}', f'confirm_leave:{selected_phone}'.encode())],
                [Button.inline('❌ إلغاء', b'cancel_leave')]
            ]
            await event.edit(
                f'⚠️ **هل أنت متأكد من مغادرة جميع المجموعات لحساب {selected_acc["name"]}؟**\n'
                'هذه العملية لا يمكن التراجع عنها!',
                buttons=buttons
            )
    except Exception as e:
        await event.respond(f'حدث خطأ: {str(e)}')


@client.on(events.CallbackQuery(pattern=rb'confirm_leave:(.*)'))
async def confirm_leave(event):
    try:
        target_phone = event.pattern_match.group(1).decode()
        accounts = await load_accounts()
        await event.edit('⏳ جاري معالجة الطلب...')
        accounts_to_process = []
        if target_phone == 'all':
            accounts_to_process = accounts
        else:
            selected_acc = next((acc for acc in accounts if acc['phone'] == target_phone), None)
            if selected_acc:
                accounts_to_process = [selected_acc]
        if not accounts_to_process:
            await event.edit("❌ لم يتم العثور على الحسابات المطلوبة!")
            return
        total_left = 0
        total_errors = 0
        account_results = []
        for account in accounts_to_process:
            acc_name = account.get('name', 'غير معروف')
            session_str = account.get('session', '')
            if not session_str:
                account_results.append(f'• حساب {acc_name}: لا توجد جلسة صالحة')
                continue
            try:
                user_client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
                await user_client.start()
                dialogs = await user_client.get_dialogs()
                groups = [d for d in dialogs if d.is_group or d.is_channel]
                total = len(groups)
                left_count = 0
                errors = 0
                message = await event.respond(f'🔍 حساب {acc_name}: تم العثور على {total} مجموعة/قناة\n⏳ جاري المغادرة...')
                for dialog in groups:
                    try:
                        if dialog.is_channel:
                            await user_client(LeaveChannelRequest(dialog.entity))
                        else:
                            await user_client(DeleteChatUserRequest(
                                chat_id=dialog.id,
                                user_id='me'
                            ))
                        left_count += 1
                        if left_count % 5 == 0:
                            await message.edit(
                                f'⏳ حساب {acc_name}: جاري المغادرة...\n'
                                f'✅ تم مغادرة: {left_count}/{total}\n'
                                f'❌ فشل في: {errors}'
                            )
                        time.sleep(1)
                    except Exception as e:
                        errors += 1
                        continue
                account_results.append(
                    f'• حساب {acc_name}: تم {left_count} | فشل {errors} | إجمالي {total}'
                )
                total_left += left_count
                total_errors += errors
                await user_client.disconnect()
            except Exception as e:
                account_results.append(f'• حساب {acc_name}: خطأ - {str(e)}')
                continue        
        result_text = '✅ **تم الانتهاء!**\n\n' + '\n'.join(account_results)
        result_text += f'\n\nالإجمالي: تم {total_left} | فشل {total_errors}'
        await event.edit(result_text)
    except Exception as e:
        await event.respond(f'حدث خطأ أثناء التنفيذ: {str(e)}')

@client.on(events.CallbackQuery(pattern=rb'cancel_leave'))
async def cancel_leave(event):
    await event.edit('❌ تم إلغاء العملية.', buttons=None)

@client.on(events.CallbackQuery(pattern=rb'collect_active_members'))
async def collect_active_members_handler(event):
    try:
        await event.answer("تم اختيار: جمع الأعضاء النشطين في الدردشة")
        session = await load_sessions()
        session_str = session[0]
        async with client.conversation(event.chat_id) as conv:
            await conv.send_message("📥 الرجاء إرسال يوزر المجموعة المصدر وضع علامه @:")
            source_response = await conv.get_response()
            source_chat = source_response.text.replace("@", "").strip()
            await conv.send_message("🔢 عدد الرسائل الأخيرة المطلوب تحليلها (حتى 20,000):")
            limit_response = await conv.get_response()
            try:
                max_messages = min(int(limit_response.text), 200000)
            except:
                max_messages = 200000
        user_client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
        await user_client.start()
        processing_msg = await event.edit("🔄 جاري جمع الأعضاء النشطين من الدردشة...")
        try:
            source_entity = await user_client.get_entity(source_chat)
            clean_chat_name = re.sub(r'[\\/*?:"<>|]', '', source_chat.replace("https://t.me/", ""))
            filename = f"active_members_{clean_chat_name}.txt"
            filename = os.path.abspath(filename)
            
            try:
                await user_client(JoinChannelRequest(source_entity))
            except Exception as e:
                print(f"⚠️ {e}")
            members = set()
            processed_messages = 0
            async for message in user_client.iter_messages(
                source_entity,
                limit=max_messages
            ):
                if message and hasattr(message, 'sender') and message.sender:
                    if (hasattr(message.sender, 'bot') and not message.sender.bot) or not hasattr(message.sender, 'bot'):
                        if hasattr(message.sender, 'id'):
                            members.add(message.sender.id)
                        
                processed_messages += 1
                if processed_messages % 50 == 0:
                    await processing_msg.edit(
                        f"🔄 تم تحليل {processed_messages} رسالة\n"
                        f"🔍 تم جمع {len(members)} عضو نشط"
                    )
            members_count = 0
            with open(filename, 'w', encoding='utf-8') as f:
                for user_id in members:
                    try:
                        member = await user_client.get_entity(user_id)
                        user_info = []
                        if hasattr(member, 'username') and member.username:
                            user_info.append(f"{member.username}")
                        f.write("".join(user_info) + "\n")
                        members_count += 1
                    except Exception as e:
                        print(f"خطأ في جلب معلومات العضو {user_id}: {e}")
            buttons = [
                [Button.inline("📥 تحميل الملف", data=f'downloaad_{filename}')],
                [Button.inline("🔙 عودة", b'back')]
            ]
            await event.edit(
                f"✅ تم الانتهاء!\n"
                f"📊 عدد الأعضاء النشطين: {members_count}\n"
                f"📝 من خلال تحليل {processed_messages} رسالة\n"
                f"💾 الملف: {os.path.basename(filename)}",
                buttons=buttons
            )
        except Exception as e:
            await event.edit(f"❌ خطأ في الجمع: {str(e)}")
        finally:
            await user_client.disconnect()
    except Exception as e:
        await event.edit(f"❌ حدث خطأ: {str(e)}")


@client.on(events.CallbackQuery(pattern=rb'download_(.*)'))
async def download_handler(event):
    try:
        filename = event.pattern_match.group(1).decode()
        safe_filename = os.path.abspath(filename)
        if os.path.exists(safe_filename):
            await event.respond(file=safe_filename, attributes=[DocumentAttributeFilename(os.path.basename(safe_filename))])
            await event.answer("✅ تم إرسال الملف بنجاح")
        else:
            await event.answer("❌ الملف غير موجود")
    except Exception as e:
        await event.answer(f"❌ فشل إرسال الملف: {str(e)}")

@client.on(events.CallbackQuery(pattern=rb'download_(.*)'))
async def download_handler(event):
    filename = event.pattern_match.group(1).decode()
    try:
        await event.respond(file=filename, attributes=[DocumentAttributeFilename(filename)])
        await event.answer("✅ تم إرسال الملف بنجاح")
    except Exception as e:
        await event.answer(f"❌ فشل إرسال الملف: {str(e)}")


@client.on(events.CallbackQuery(data=b'transss'))
async def trs_handler(event):
    try:
        stop_event.clear()
        async with client.conversation(event.chat_id, timeout=300) as conv:
            await conv.send_message("📁 **الرجاء إرسال ملف txt يحتوي على اليوزرنيمز (كل يوزر في سطر):**")
            file_response = await conv.get_response()
            
            if not file_response.file:
                await conv.send_message("❌ لم يتم إرسال ملف، الرجاء المحاولة مرة أخرى")
                return
            
            file_path = await file_response.download_media()
            
            await conv.send_message("🔢 **الرجاء إدخال عدد الأعضاء المراد نقلهم:**\n(مثال: 50)")
            number_response = await conv.get_response()
            number = min(int(number_response.text.strip()), 20000)

            await conv.send_message("📤 **الرجاء إدخال رابط المجموعة الهدف:**\n(مثال: @sghiiuyggh أو https://t.me/sghiiuyggh)")
            target_response = await conv.get_response()
            target_chat = target_response.text.replace("@", "").replace("https://t.me/", "").strip()
            
        processing_msg = await event.edit("🔄 جاري بدء العملية...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                usernames = [line.strip() for line in f.readlines() if line.strip()]
            os.remove(file_path)
        except Exception as e:
            await event.edit(f"❌ خطأ في قراءة الملف: {str(e)}")
            return
        
        max_per_acc = 49
        count = 0
        added_users = set()
        failed_users = set()
        skipped_users = set()
        sessions = await load_sessions()

        if not sessions:
            await event.edit("❌ لا توجد جلسات في ملف sessions.txt")
            return

        with open('data.txt', 'a', encoding='utf-8') as trans_file:
            start_time = time.time()
            processed_accounts = 0

            for session_str in sessions:
                if stop_event.is_set():
                    break
                
                if count >= len(usernames):
                    break

                if count >= number:
                    break

                user = TelegramClient(StringSession(session_str), API_ID, API_HASH)
                processed_accounts += 1
                
                try:
                    await user.start()
                    me = await user.get_me()
                    account_name = f"@{me.username}" if me.username else f"user_id:{me.id}"
                    print(f"🔹 بدأت جلسة للحساب: {account_name}")

                    try:
                        target_entity = await user.get_entity(target_chat)
                    except Exception as e:
                        print(f"❌ خطأ في الحصول على الكيان الهدف: {str(e)}")
                        continue

                    try:
                        await user(JoinChannelRequest(target_entity))
                        print(f"   ✅ انضم إلى الهدف: {target_chat}")
                    except UserAlreadyParticipantError:
                        print(f"   ℹ️ الحساب موجود بالفعل في الهدف")
                    except Exception as e:
                        print(f"   ❌ خطأ في الانضمام للهدف: {str(e)}")
                        continue

                    await asyncio.sleep(3)

                    try:
                        current_account_added = 0
                        
                        for username in usernames[count:]:
                            if current_account_added >= max_per_acc:
                                break

                            if count >= number:
                                break

                            if stop_event.is_set():
                                break

                            if username in failed_users:
                                continue
                            
                            if username in added_users or username in skipped_users:
                                continue

                            try:
                                member = await user.get_entity(username)
                                
                                try:
                                    await user(GetParticipantRequest(target_entity, member))
                                    skipped_users.add(username)
                                    print(f"   ⏩ تخطي عضو موجود: @{username}")
                                    continue
                                except:
                                    pass

                                try:
                                    await asyncio.sleep(1)
                                    await user(InviteToChannelRequest(
                                        target_entity,
                                        [member]
                                    ))
                                    await asyncio.sleep(1)
                                    try:
                                        participant = await user(GetParticipantRequest(target_entity, member))
                                        if participant and hasattr(participant, 'participant'):
                                            added_users.add(username)
                                            count += 1
                                            current_account_added += 1
                                            print(f"   ✅ تمت إضافة عضو بنجاح: @{username}")
                                            trans_file.write(f"{username}\n")
                                            trans_file.flush()
                                        else:
                                            failed_users.add(username)
                                            print(f"   ❌ لم يتم العثور على العضو بعد الإضافة: @{username}")
                                    except Exception as e:
                                        failed_users.add(username)
                                        print(f"   ❌ فشل التحقق من العضو المضاف: @{username} - {str(e)}")
                                    
                                    delay = max(2, min(10, 60 / max_per_acc))
                                    await asyncio.sleep(delay)
                                except UserAlreadyParticipantError:
                                    skipped_users.add(username)
                                    print(f"   ⏩ تخطي عضو موجود: @{username}")
                                except FloodWaitError as fwe:
                                    break
                                except Exception as e:
                                    failed_users.add(username)
                                    print(f"   ❌ فشل إضافة عضو @{username}: {str(e)}")
                                    await asyncio.sleep(5)

                            except Exception as e:
                                failed_users.add(username)
                                print(f"   ❌ خطأ في جلب معلومات @{username}: {str(e)}")
                                continue

                    except Exception as e:
                        print(f"❌ خطأ في جلب الأعضاء: {str(e)}")
                    
                    try:
                        await client.send_message(
                            event.chat_id,
                            f"📊 **تقرير الحساب {account_name}**\n"
                            f"✅ تمت إضافة: {current_account_added} عضو\n"
                            f"⏩ تم تخطي: {len([u for u in skipped_users if u not in added_users])} عضو (موجودين مسبقاً)\n"
                            f"❌ فشل في إضافة: {len([u for u in failed_users if u not in skipped_users])} عضو\n"
                            f"🔢 الإجمالي حتى الآن: {count}/{len(usernames)}"
                        )
                    except Exception as e:
                        print(f"❌ فشل إرسال تقرير الحساب: {str(e)}")

                except Exception as e:
                    print(f"❌ خطأ عام في الجلسة: {str(e)}")
                finally:
                    try:
                        await user.disconnect()
                    except:
                        pass

        elapsed_time = int(time.time() - start_time)
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        result_message = (
            f"🎉 **النتائج النهائية**\n\n"
            f"⏱️ المدة: {time_str}\n"
            f"🔢 العدد المستهدف: {len(usernames)} عضو\n"
            f"✅ تمت إضافة: {count} عضو\n"
            f"⏩ تم تخطي: {len(skipped_users)} عضو (موجودين مسبقاً)\n"
            f"❌ فشل في إضافة: {len(failed_users)} عضو\n"
            f"👥 عدد الحسابات المستخدمة: {processed_accounts}\n\n"
            f"🎯 الهدف: {target_chat}\n"
            f"💾 تم حفظ اليوزرنيمز المنقولة في ملف: trans.txt"
        )

        try:
            await client.send_message(
                event.chat_id,
                result_message,
                buttons=[Button.inline("🔙 العودة", b"back_to_main")]
            )
            await processing_msg.delete()
        except Exception as e:
            print(f"❌ فشل إرسال التقرير النهائي: {str(e)}")
            await processing_msg.edit(
                result_message,
                buttons=[Button.inline("🔙 العودة", b"back_to_main")]
            )

    except Exception as e:
        error_msg = f"❌ حدث خطأ غير متوقع:\n{str(e)}"
        try:
            await client.send_message(
                event.chat_id,
                error_msg,
                buttons=[Button.inline("🔙 العودة", b"back_to_main")]
            )
        except:
            await event.edit(
                error_msg,
                buttons=[Button.inline("🔙 العودة", b"back_to_main")]
            )

async def main():
    await client.start(bot_token=bot_token)
    print("البوت شغال ✅")
    await client.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
