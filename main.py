from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('TOKEN_BOT')
app = ApplicationBuilder().token(token).build()

# Iniciales para MLC
mlc_prefixes = [
    '9225', '9235', '9245', '9226', '9228', '9229',
]

# Iniciales para CUP
cup_prefixes = [
    '9200', '9204', '9205', '9206', '9224', '9212', 
    '9213', '9238', '9237', '9227', '9234', '9202'
]

# Función para identificar el tipo de tarjeta
def identificar_tipo_tarjeta(numero_tarjeta):
    # Elimina los espacios para analizar el número
    print(f"Numero tarjeta: {numero_tarjeta}")
    numero_tarjeta = numero_tarjeta.replace(" ", "")
    
    # Extraer los primeros cuatro dígitos
    prefijo = numero_tarjeta[:4]
    
    # Verificar si el prefijo corresponde a MLC o CUP
    if prefijo in mlc_prefixes:
        return "MLC"
    elif prefijo in cup_prefixes:
        return "CUP"
    else:
        return "Tipo de tarjeta desconocido"

# Función para identificar el banco a partir del número de tarjeta
def identificar_banco(numero_tarjeta):
    # Elimina los espacios en blanco para analizar el número
    numero_tarjeta = numero_tarjeta.replace(" ", "")
    numero_tarjeta = numero_tarjeta.replace("-", "")
    
    if len(numero_tarjeta) != 16:
        return "El número de tarjeta debe tener 16 dígitos."
    # Extraer los dígitos del 4 al 8 (índice 3 al 7 en Python)
    bloque = numero_tarjeta[4:8]
    
    # Identificar el banco
    if bloque == '9598':
        return "Metropolitano"
    elif bloque == '1299':
        return "BPA"
    elif bloque == '0699':
        return "BANDEC"
    else:
        return "Desconocido"

# Función para manejar los mensajes de los usuarios
async def handle_message(update: Update, context):
    numero_tarjeta = update.message.text
    banco = identificar_banco(numero_tarjeta)
    tipo_tarjeta = identificar_tipo_tarjeta(numero_tarjeta)

    if numero_tarjeta == "/start":
        await update.message.reply_text("Para obtener detalles sobre una tarjeta, escriba el número de la misma")
        return

    detalles = {
        "Banco": banco,
        "Tipo de tarjeta": tipo_tarjeta
    }
    respuesta = ""
    for key, value in detalles.items():
        respuesta += f"{key}: {value}\n"

    await update.message.reply_text(respuesta)

# Manejador para todos los mensajes de texto
app.add_handler(MessageHandler(filters.TEXT, handle_message))
# Iniciar el bot
if __name__ == '__main__':
    os.system("clear")
    print("Tarjetas Telegram Bot iniciado\n")
    # logger.info("Bot running...")
    app.run_polling()