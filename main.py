import os
from telethon import TelegramClient, events
import openai

# Set up environment variables
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the Telegram client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Define a handler for new messages
@client.on(events.NewMessage)
async def handle_message(event):
    # Get the message text
    user_message = event.message.message

    # Send the message to OpenAI and get a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=150
    )
    assistant_response = response.choices[0].text.strip()

    # Send the response back to the user
    await event.reply(assistant_response)

# Start the Telegram client
client.start()
client.run_until_disconnected()
