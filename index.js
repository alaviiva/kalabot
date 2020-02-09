
require('dotenv').config();

const chance = require('chance').Chance();
const TelegramBot = require('node-telegram-bot-api');
const token = process.env.TG_API_TOKEN;
const bot = new TelegramBot(token, {polling: true});

bot.onText(/\/kala/, (msg) => {
  bot.sendMessage(msg.chat.id, 'Olet kala');
});

bot.onText(/\/roll (.+)/, (msg, match) => {
  console.log(match[1]);
  const result = chance.rpg(match[1], {sum: true});
  bot.sendMessage(msg.chat.id, result);
});

bot.on('polling_error', (error) => {
  console.log(error);
});
