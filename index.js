
require('dotenv').config();

const TelegramBot = require('node-telegram-bot-api');
const token = process.env.TG_API_TOKEN;
const bot = new TelegramBot(token, {polling: true});
console.log("start");

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, "Kala");
});

bot.onText(/\/kala/, (msg) => {
  bot.sendMessage(msg.chat.id, "Olet kala");
});
