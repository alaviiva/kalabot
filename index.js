
require('dotenv').config();

const chance = require('chance').Chance();
const TelegramBot = require('node-telegram-bot-api');
const token = process.env.TG_API_TOKEN;
const bot = new TelegramBot(token, {polling: true});

const suits = ['♠️ ', '♣️ ', '♥️ ', '♦️ '];
const cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];

bot.onText(/\/kala/, (msg) => {
  bot.sendMessage(msg.chat.id, 'Olet kala');
});

bot.onText(/\/roll (\d*d\d+)/, (msg, match) => {
  //console.log(match);
  var d = match[1];
  if (d.startsWith('d')) {
    d = '1' + d;
  }
  const result = chance.rpg(d, {sum: true});
  bot.sendMessage(msg.chat.id, result);
});

bot.onText(/\/kortti/, (msg) => {
  const n = chance.integer({min: 0, max: 53});

  var result = '';

  if (n > 51) {
    result = '🃏';
  } else {
    result = suits[Math.floor(n / 13)] + cards[n % 13];
  }

  bot.sendMessage(msg.chat.id, result);
});

bot.on('polling_error', (error) => {
  console.log(error);
});
