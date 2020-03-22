import json
import telegram
import os
import logging
import random
import re


# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, something went wrong!')
}

SUITS = ['♠️ ', '♣️ ', '♥️ ', '♦️ ']
CARDS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def configure_telegram():
    """
    Configures the bot with a Telegram Token.

    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)


def webhook(event, context):
    """
    Runs the Telegram webhook.
    """

    bot = configure_telegram()
    logger.info('Event: {}'.format(event))

    if event.get('httpMethod') == 'POST' and event.get('body'):
        logger.info('Message received')
        update = telegram.Update.de_json(json.loads(event.get('body')), bot)
        chat_id = update.message.chat.id
        text = update.message.text
        resp = ''

        if text == '/start':
            resp = 'Olet kala'

        if text.startswith('/kortti'):
            resp = kortti(text)

        if text.startswith('/roll'):
            resp = roll(text)

        if resp != '':
            bot.sendMessage(chat_id=chat_id, text=resp)
            logger.info('Message sent')

        return OK_RESPONSE

    return ERROR_RESPONSE

def kortti(text):
    n = random.randint(0, 53)
    if n > 51:
        resp = '🃏'
    else:
        resp = SUITS[n // 13] + CARDS[n % 13]

    return resp

def roll(text):
    p = re.compile(r'\d*d\d+')
    m = p.search(text)

    if not m:
        return random.randint(1, 100)

    s = m.group().split('d')
    if s[0] == '':
        s[0] = 1
    s[0] = int(s[0])
    s[1] = int(s[1])

    if s[1] < 1:
        return 'invalid'

    sum = 0
    for i in range(s[0]):
        sum += random.randint(1, s[1])

    return sum

def set_webhook(event, context):
    """
    Sets the Telegram bot webhook.
    """

    logger.info('Event: {}'.format(event))
    bot = configure_telegram()
    url = 'https://{}/{}/'.format(
        event.get('headers').get('Host'),
        event.get('requestContext').get('stage'),
    )
    webhook = bot.set_webhook(url)

    if webhook:
        return OK_RESPONSE

    return ERROR_RESPONSE
