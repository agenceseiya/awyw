const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

// Initialize the bot with your Telegram API token
const bot = new TelegramBot(process.env.TELEGRAM_API_TOKEN, { polling: true });

// Listen for any kind of message
bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const userMessage = msg.text;

  try {
    // Send the user message to the custom GPT model
    const openaiResponse = await axios.post(
      'https://api.openai.com/v1/engines/davinci-codex/completions',
      {
        prompt: userMessage,
        max_tokens: 50,
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
        },
      }
    );

    const responseText = openaiResponse.data.choices[0].text.trim();

    // Send the response back to the user
    bot.sendMessage(chatId, responseText);
  } catch (error) {
    console.error('Error handling message:', error);
    bot.sendMessage(chatId, 'Sorry, an error occurred. Please try again later.');
  }
});
