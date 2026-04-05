#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Myanmar Telegram Bots - Main Application
Runs both Group Management Bot and AI Assistant Bot
"""
import os
import asyncio
import logging
from telegram.ext import Application
from dotenv import load_dotenv
import signal
import sys

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get tokens from environment variables
GROUP_BOT_TOKEN = os.getenv('GROUP_BOT_TOKEN')
AI_BOT_TOKEN = os.getenv('AI_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not GROUP_BOT_TOKEN or not AI_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Missing required environment variables: GROUP_BOT_TOKEN, AI_BOT_TOKEN, or OPENAI_API_KEY")

# Global application instances
group_app = None
ai_app = None

async def main():
    """Start both bots"""
    global group_app, ai_app
    
    logger.info("Starting Myanmar Telegram Bots...")
    
    # Create applications for both bots
    group_app = Application.builder().token(GROUP_BOT_TOKEN).build()
    ai_app = Application.builder().token(AI_BOT_TOKEN).build()
    
    # Add handlers for group management bot
    from handlers.group_handlers import setup_group_handlers
    setup_group_handlers(group_app)
    
    # Add handlers for AI assistant bot
    from handlers.ai_handlers import setup_ai_handlers
    setup_ai_handlers(ai_app)
    
    # Start both bots concurrently
    logger.info("Starting Group Management Bot...")
    logger.info("Starting AI Assistant Bot...")
    
    try:
        # Run both applications concurrently
        await asyncio.gather(
            group_app.run_polling(),
            ai_app.run_polling()
        )
    except Exception as e:
        logger.error(f"Error running bots: {e}")
        raise

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    logger.info("Received shutdown signal")
    if group_app:
        asyncio.run(group_app.stop())
    if ai_app:
        asyncio.run(ai_app.stop())
    sys.exit(0)

if __name__ == '__main__':
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
