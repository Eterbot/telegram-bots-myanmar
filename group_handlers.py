#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Group Management Bot Handlers - Myanmar Language Support
"""

import logging
from telegram import Update, ChatMember
from telegram.ext import ContextTypes, ChatMemberHandler, MessageHandler, filters
from telegram.constants import ChatMemberStatus

logger = logging.getLogger(__name__)

# Myanmar welcome message
WELCOME_MESSAGE = """
ကြိုးဆိုကျေးဇူးပြု၍ ကျွန်တော်တို့ အုပ်စုသို့ ကြိုးဆိုပါသည်။ 🎉

အုပ်စုမှ စည်းကမ်းများ -
✅ အရုပ်စကား မပြောပါ
✅ အစ်ကို/အမ အီသုံးပြီး စကားပြောပါ
✅ အဆန်းတဲ့ လင့်ခ်များ မဝေမျှပါ
✅ အခြား အုပ်စုများသို့ အဖိုးအခြင်း မဆွဲခြင်းပါ

ကျွန်တော်တို့ အုပ်စုကို ပူးပေါင်းဆောင်ရွက်ပြီး ကျေးဇူးတင်ပါသည်။
"""

SPAM_WARNING = "⚠️ အဆန်းတဲ့ လင့်ခ်များ မဝေမျှပါ။ ထပ်မံ ပြုမူလျှင် အုပ်စုမှ ဖယ်ထုတ်ခံရလိမ့်မည်။"

async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greet new members joining the group"""
    result = update.chat_member
    
    if result.new_chat_member.status == ChatMemberStatus.MEMBER:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=WELCOME_MESSAGE,
                parse_mode='HTML'
            )
            logger.info(f"Welcomed new member: {result.new_chat_member.user.first_name}")
        except Exception as e:
            logger.error(f"Error sending welcome message: {e}")

async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check for spam links and warn users"""
    if not update.message or not update.message.text:
        return
    
    spam_keywords = ['http://', 'https://', 'tinyurl', 'bit.ly', 'short.link']
    text = update.message.text.lower()
    
    if any(keyword in text for keyword in spam_keywords):
        try:
            await update.message.reply_text(SPAM_WARNING)
            logger.warning(f"Spam detected from {update.effective_user.first_name}")
        except Exception as e:
            logger.error(f"Error handling spam: {e}")

def setup_group_handlers(app):
    """Setup all handlers for group management bot"""
    # Handle new members
    app.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.MY_CHAT_MEMBER))
    
    # Check for spam
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spam))
    
    logger.info("Group management handlers setup complete")
