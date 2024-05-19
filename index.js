const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

const bot = new TelegramBot(process.env.TELEGRAM_API_TOKEN, { polling: true });

bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const userMessage = msg.text;

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

  const responseText = openaiResponse.data.choices[0].text;

  bot.sendMessage(chatId, responseText);
});
