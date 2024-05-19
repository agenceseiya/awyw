const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

// Initialize the bot with your Telegram API token
const bot = new TelegramBot(process.env.TELEGRAM_API_TOKEN, { polling: true });

// Listen for any kind of message
bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const userMessage = msg.text;

  try {
    // Send the user message to your custom assistant
    const assistantResponse = await axios.post(
      process.env.ASSISTANT_API_URL,
      {
        prompt: userMessage,
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.ASSISTANT_API_KEY}`,
        },
      }
    );

    const responseText = assistantResponse.data.reply; // Adjust based on your API response structure

    // Send the response back to the user
    bot.sendMessage(chatId, responseText);
  } catch (error) {
    console.error('Error handling message:', error);
    bot.sendMessage(chatId, 'Sorry, an error occurred. Please try again later.');
  }
});
