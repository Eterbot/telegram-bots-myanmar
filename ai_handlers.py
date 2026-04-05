#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Assistant Bot Handlers - Myanmar Language Support with OpenAI
"""

import logging
import os
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Myanmar system prompt for AI
SYSTEM_PROMPT = """
သင်သည် အဆင်သည်းတဲ့ အကူအညီ ပေးသည့် Myanmar AI အကူအညီ အစ်ကို/အမ ဖြစ်သည်။
Myanmar ဘာသာစကားဖြင့် လူမှုကွန်ယက်မှ အမေးအမြန်းများအပြီး အကူအညီ ပေးပါ။
အမေးအမြန်းများကို လေးစားမှုရှိစွာ ဖြေဆိုပါ။
"""

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    welcome_text = """
ကြိုးဆိုပါသည်။ 👋

ကျွန်တော်သည် Myanmar AI အကူအညီ အစ်ကို/အမ ဖြစ်ပါသည်။
သင်၏ မေးခွန်းများကို Myanmar ဘာသာစကားဖြင့် မေးပြီး 
ကျွန်တော်သည် အကူအညီ ပေးပါ့မည်။

မည်သည့် အကူအညီ လိုအပ်ပါသလဲ? 🤔
"""
    await update.message.reply_text(welcome_text)
    logger.info(f"User {update.effective_user.first_name} started the bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
ကျွန်တော်ကို အကူအညီ ပေးနိုင်သည့် အရာများ - 📚

✅ အယ်လ်အီ အမေးအမြန်းများ ဖြေဆိုခြင်း
✅ Myanmar ဘာသာစကား ဆက်သွယ်မှု
✅ အချက်အလက် ရှာဖွေခြင်း
✅ အဆင်သည်းတဲ့ အကူအညီ ပေးခြင်း

မည်သည့် အကူအညီ လိုအပ်ပါသလဲ?
"""
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages and respond with AI"""
    if not update.message or not update.message.text:
        return
    
    user_message = update.message.text
    
    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content
        
        # Send response (split if too long)
        if len(ai_response) > 4096:
            for i in range(0, len(ai_response), 4096):
                await update.message.reply_text(ai_response[i:i+4096])
        else:
            await update.message.reply_text(ai_response)
        
        logger.info(f"Responded to {update.effective_user.first_name}")
        
    except Exception as e:
        error_message = "အခု အကူအညီ ပေးနိုင်မရှိပါ။ အနည်းငယ်အချိန်ကြာပြီး ထပ်မံ ကြိုးစားပါ။"
        await update.message.reply_text(error_message)
        logger.error(f"Error calling OpenAI API: {e}")

def setup_ai_handlers(app):
    """Setup all handlers for AI assistant bot"""
    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("AI assistant handlers setup complete")
