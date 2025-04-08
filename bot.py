
import telebot
from telebot import types

ADMIN_ID = 7515320314
BOT_TOKEN = '7524372968:AAGXu4RA6kqkVHKo1fIuf4_Vs8CqdbNKzTE'
bot = telebot.TeleBot(BOT_TOKEN)

# Chave Pix e imagem do QR Code
PIX_KEY = "ccd821c8-0894-45c0-8f8b-b945bd9c9c09"
QR_CODE_IMAGE = "qrcode_pix_atualizado.png"

# Valores dos produtos
PRECO_CAMISA = 150
PRECO_TENIS = 120
PRECO_COMBO = 250

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('👕 Comprar Camisa', '👟 Comprar Tênis')
    markup.add('🧢 Combo Camisa + Tênis')
    bot.send_message(message.chat.id, "Olá! Bem-vindo(a)!\nEscolha o que deseja:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ['👕 Comprar Camisa', '👟 Comprar Tênis', '🧢 Combo Camisa + Tênis'])
def handle_purchase(message):
    if message.text == '👕 Comprar Camisa':
        valor = PRECO_CAMISA
    elif message.text == '👟 Comprar Tênis':
        valor = PRECO_TENIS
    else:
        valor = PRECO_COMBO

    caption = f"💵 *Pagamento*\n\n🧾 Valor: R${valor}\n🔑 Chave Pix: `{PIX_KEY}`\n\nApós o pagamento, envie o comprovante aqui mesmo."
    with open(QR_CODE_IMAGE, 'rb') as qr:
        bot.send_photo(message.chat.id, qr, caption=caption, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    if message.reply_to_message:
        return
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "📩 Comprovante recebido! Aguarde a confirmação do administrador.")

@bot.message_handler(commands=['autorizar'])
def autorizar_entrega(message):
    if message.from_user.id == ADMIN_ID:
        if message.reply_to_message:
            bot.send_message(message.reply_to_message.forward_from.id, "✅ Pagamento confirmado! Produto será enviado em breve.")
        else:
            bot.reply_to(message, "Responda ao comprovante para autorizar a entrega.")

bot.infinity_polling()
