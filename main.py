import os
from telethon import TelegramClient, events
import openai
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Set up environment variables
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not all([API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY]):
    logging.error("One or more environment variables are missing")
    raise ValueError("One or more environment variables are missing")

# Initialize the Telegram client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Log the bot start
logging.info("Bot started")

# Define a handler for the /start command
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    logging.info(f"Received /start from {event.sender_id}")
    await event.reply("Hello! How can I assist you today?")

# Define a handler for new messages
@client.on(events.NewMessage)
async def handle_message(event):
    # Get the message text
    user_message = event.message.message
    logging.info(f"Received message: {user_message} from {event.sender_id}")

    # Send the message to OpenAI and get a response
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_message,
            max_tokens=150
        )
        assistant_response = response.choices[0].text.strip()
        logging.info(f"OpenAI response: {assistant_response}")

        # Send the response back to the user
        await event.reply(assistant_response)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await event.reply("Sorry, something went wrong.")

# Start the Telegram client
client.start()
client.run_until_disconnected()
