import telebot
from telebot import types
from configuracion import *

#Conexion con el bot
TOKEN = Token_bot
bot = telebot.TeleBot(TOKEN)



#creacion de comandos /help y /star
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,'Hola, soy un bot de Xtables pc dime en que te puedo ayudar?')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,'Debe interactuar con el bot con el comando /options para inicar las consultas')


#Menu de opciones
def teclado_options(opciones):
    # Crear botones con callback_data
        teclado = types.InlineKeyboardMarkup()
        for texto, callback_data in opciones:
            boton = types.InlineKeyboardButton(text=texto, callback_data=callback_data)
            teclado.add(boton)

        return teclado
#menu de opciones
@bot.message_handler(commands=['options'])
def send_option(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    #creacion de botones
    btn_consulta = types.InlineKeyboardButton('Consulta sobre Programas', callback_data='consultas')
    btn_promociones = types.InlineKeyboardButton('Promociones y Descuentos', callback_data='promociones')
    btn_compra = types.InlineKeyboardButton('Proceso de Compra', callback_data='compra')
    btn_soporte = types.InlineKeyboardButton('Soporte y Ayuda', callback_data='soporte')
    btn_busqueda = types.InlineKeyboardButton('Busqueda Personalizada', callback_data='busqueda')

    #Agrega botones al markup
    markup.add(btn_consulta,btn_promociones,btn_compra,btn_soporte,btn_busqueda)

    #envia mensaje con los botones
    bot.send_message(message.chat.id,'Elija alguna de las opciones',reply_markup=markup)

#Menu de los distintos programas
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    #Consulta de opciones
    if call.data == 'consultas':
        opciones = [
            ("Utilidad ✔", "info_utilidad"),
            ("Portables 💽", "info_portables"),
            ("Negocios 💼", "info_negocios"),
            ("Oficina 📈", "info_oficina"),
            ("Diseño 🎨", "info_diseño"),
            ("Video 🎥", "info_video"),
            ("Audio 🎶", "info_audio")
        ]
        teclado = teclado_options(opciones)
        bot.send_message(call.message.chat.id, "📂 Categorías de Software disponibles.\nSelecciona una opción para más información:", reply_markup=teclado)

    #promociones
    elif call.data == 'promociones':
        eventos = [
            ("Navidad 🎄", "info_navidad"),
            ("Año Nuevo 🎉", "info_new"),
            ("Black Friday ⚫", "info_black"),
            ("Inicios de Verano ⛱", "info_summer"),
            ("San Valentín 💘", "info_san"),
            ("Regreso a Clases 📚", "info_class")
        ]
        teclado = teclado_options(eventos)
        bot.send_message(call.message.chat.id, "🎉 Promociones y descuentos disponibles.\nSelecciona una opción para más información:", reply_markup=teclado)
    
    #mensaje de Compra
    elif call.data == 'compra':
        bot.send_message(
            call.message.chat.id, 
            "El metodo de Compra es sencillo y constas de 2 pasos:\n" 
            "Metodo de pago:"
            "La venta del programa es totalmente online mendiante Paypal para garantizar la seguridad del cliente y proveedor" 
            "Llegada del Producto:* \nSe proporcionara un recurso para realizar el respectiva entrega del producto"
            "En caso de tener más dudas Visite la pagina oficial" 
            "https://xtables.wordpress.com/", 
            parse_mode="Markdown")

    #Ayuda y Soporte
    elif call.data == 'soporte':
        bot.send_message(
            call.message.chat.id,
            "En caso de tener preguntas o problemas con el programa, contactese al siguiente correo:\n"
            "xtablespc@gmail.com\n"
            "Los mensajes deben ser en horario habil de:\n 8 am a 10 pm GT\n"
            "Únete a nuestro canal de Telegram para estar enterado de las últimas actualizaciones:\n"
            "https://t.me/xtablespc")
        
    #busqueda personalizada
    elif call.data == 'busqueda':
# Mensaje dinámico con una búsqueda
        bot.send_message(
            call.message.chat.id,
            "Ingrese el nombre del programa a buscar"
        )

        

    # Unificar todas las respuestas de "info_" en un solo diccionario
    info = {
        # Información de Software
        "info_utilidad": "🔹 https://xtables.wordpress.com/category/utilitarios/",
        "info_portables": "💽 https://xtablespc.blogspot.com/",
        "info_negocios": "💼 https://xtables.wordpress.com/category/negocios/",
        "info_oficina": "📈 https://xtables.wordpress.com/category/oficina/",
        "info_diseño": "🎨 https://xtables.wordpress.com/category/diseno/",
        "info_video": "🎥 https://xtables.wordpress.com/category/video/",
        "info_audio": "🎶 https://xtables.wordpress.com/category/audio/",
        
        # Información de Promociones
        "info_navidad": "🎄 Descuentos de Navidad: del 15 al 27 de diciembre.",
        "info_new": "🎉 Promoción de Año Nuevo: del 30 de diciembre al 5 de enero.",
        "info_black": "⚫ Black Friday: finales de noviembre.",
        "info_summer": "⛱ Rebajas de verano: primeros 10 días de la temporada.",
        "info_san": "💘 Descuentos por San Valentín: todo febrero.",
        "info_class": "📚 Promoción regreso a clases: del 1 al 15 de septiembre."
    }

    # Si el callback es de tipo "info_", responder con el mensaje correspondiente
    if call.data.startswith("info_"):
        mensaje = info.get(call.data, "❌ Opción no encontrada. Inténtalo nuevamente.")
        bot.send_message(call.message.chat.id, mensaje)


#Busqueda de programas
# Mensaje dinámico con una búsqueda
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if(message == ''):
        bot.reply_to(message,'Lo siento debes poner un nombre real')
    else:
        busqueda = message.text  # Puedes obtener esto de un usuario, por ejemplo, desde un handler de mensajes
        url = f"https://xtables.wordpress.com/?s={busqueda}"
        url_2 = f"https://7pc7.blogspot.com/search?q={busqueda}"

        # Formato Markdown (correcto)
        mensaje = f"Visita nuestro sitio web: [Haz clic aquí]({url})" 
        bot.reply_to(message,'Aqui tienes la pagina oficial de XtablesPc para que tengas más informacion.')
        bot.send_message(message.chat.id,mensaje)

        mensaje2 = f"O visita otro sitio web: [Haz clic aquí]({url_2})"
        bot.reply_to(message,'Aqui tienes la pagina oficial de XtablesPc para que tengas más informacion.')
        bot.send_message(message.chat.id,mensaje2)         

#validad que se ejecute el archivo main
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Error: {e}")
    