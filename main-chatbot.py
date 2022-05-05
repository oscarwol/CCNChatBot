"""
- NPL ChatBot: Cerveceria Nicaraguence (Promociones & Comunicacion Continua)
- Version: 1.0
- Created for: WOL Media & Digital Division (soportedev@wol.group)
- License: Wol Media Copyrighted Software
- Author: Oscar E. Morales (oscarmoralesgt.com)

- Rights reserved, This program and code is issued for the purposes that the interested party deems appropriate.
"""

# Importamos las librerias y paquetes necesarios
from re import I
import smtplib
from telegram import (
    Update,
    Sticker,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    ParseMode,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    ConversationHandler,
)
import requests

updater = Updater("TOKENHERE")
reply_keyboard = [["stickers", "fondos"], ["musica", "promociones"]]
promo_keyboard = [["1", "2"], ["3", "4"]]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
markup_promo = ReplyKeyboardMarkup(promo_keyboard, one_time_keyboard=True)


# Funcion de Inicio (Disparador / Trigger)
def start(update: Update, context: CallbackContext) -> None:
    context.user_data["estado"] = "Menu:Inicial"
    context.user_data["datos_usuario"] = {"CUI": None, "correo": None}
    MenuInicial(update, context)
    SeleccionPorNumero(update, context)


# Funcion que nos permite seleccion por numero en los diferentes menus
def SeleccionPorNumero(update, context):
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    updater.dispatcher.add_handler(echo_handler)


"""
Menus y Opciones disponibles dentro del chat
"""


def MenuInicial(update, context):
    update.message.reply_text("Gracias por comunicarte con el bot de WOL")
    update.message.reply_text(
        "Escribe 1️⃣ o *stickers* para obtener los mejores stickers de WOL",
        parse_mode=ParseMode.MARKDOWN,
    )
    update.message.reply_text(
        "Escribe 2️⃣ o *fondos* para obtener los mejores Fondos de pantalla de WOL",
        parse_mode=ParseMode.MARKDOWN,
    )
    update.message.reply_text(
        "Escribe 3️⃣ o *musica* para obtener las mejores canciones de WOL",
        parse_mode=ParseMode.MARKDOWN,
    )
    update.message.reply_text(
        "Escribe 4️⃣ o *promociones* para ver las promociones existentes o verificar tu codigo promocional",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup,
    )


def MenuPromociones(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Escribe 1️⃣ para ver las promociones de Cerveza Toña",
        parse_mode=ParseMode.MARKDOWN,
    )
    update.message.reply_text(
        "Escribe 2️⃣ para ver las promociones de Victoria & Victoria Clasica",
        parse_mode=ParseMode.MARKDOWN,
    )
    update.message.reply_text(
        "Escribe 3️⃣ para verificar tu codigo promocional de Promocion1",
        parse_mode=ParseMode.MARKDOWN,
    )
    update.message.reply_text(
        "Escribe 4️⃣ para verificar tu codigo promocional de Promocion2",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup_promo,
    )
    update.message.reply_text("Escribe 0️⃣ para regresar el Menu inicial")

    context.user_data["estado"] = "Menu:Promociones"
    context.user_data["datos_usuario"] = {"CUI": None, "correo": None}

    SeleccionPorNumero(update, context)


def VolverAlMenu(update, context):
    if context.user_data["estado"] == "Menu:Inicial":
        update.message.reply_text(
            "Escribe 0️⃣ para mostar el menu nuevamente, o elige una de las opciones anteriores"
        )
    elif context.user_data["estado"] == "Menu:Promociones":
        update.message.reply_text(
            "Escribe 5️⃣ para regresar al Menu de Promociones \nEscribe 0️⃣ para regresar al menu inicial\n"
        )
    SeleccionPorNumero(update, context)


"""
Envio de materiales multimedia
"""


def stickers(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Aqui tienes los stickers promocionales de la temporada ¡Que los disfrutes!"
    )
    lss = Sticker(
        "CAACAgEAAxkBAAEEOGliN_EjxQ19yHZx95dMHY06la3mjAACHwIAAphrwEXZfwOBZNhyJyME",
        "5026135484724675103",
        500,
        500,
        False,
        False,
    )
    lss2 = Sticker(
        "CAACAgEAAxkBAAEEOGtiN_GljWduHMmtsmIDQkCFy3kyCAACigEAAom_wUWasuCOKmTtuiME",
        "5026509254253609354",
        500,
        500,
        False,
        False,
    )
    update.message.reply_sticker(lss)
    update.message.reply_sticker(lss2)
    update.message.reply_text(
        "Haz tap en el sticker para obtener todos los stickers de WOL Media!"
    )
    VolverAlMenu(update, context)


def fondos(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Aqui tienes los fondos promocionales de la temporada ¡Que los disfrutes!"
    )
    update.message.reply_photo(
        "https://cervezatona.com/wp-content/uploads/2021/11/tona-stickers-1.png"
    )
    update.message.reply_photo(
        "https://cervezatona.com/wp-content/uploads/2021/11/cerveza-tona-botella-1.png"
    )
    update.message.reply_photo(
        "https://cervezatona.com/wp-content/uploads/2022/01/fondo-tona-8.jpg"
    )
    VolverAlMenu(update, context)


def audio(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Aqui tienes las canciones promocionales de la temporada ¡Que los disfrutes!"
    )
    update.message.reply_audio(
        "https://cervezatona.com/wp-content/uploads/2021/11/TONA_MUSICA_1-1.mp3"
    )
    update.message.reply_audio(
        "https://cervezatona.com/wp-content/uploads/2021/11/TONA_MUSICA_4.mp3"
    )
    VolverAlMenu(update, context)


"""
Seccion de Promociones y Verificacion de codigos Promocionaels:

"""


# Consumo del Endpoint de promociones y match de datos
def datosPromociones(update, context, tipo):
    endpoint = "http://127.0.0.1:5000/promos/%s" % tipo
    response = requests.get(endpoint)
    if response.status_code == 200:
        respuesta = response.json()
        for object in respuesta:
            this_nombre = object["nombre"]
            this_descripcion = object["descripcion"]
            this_url = object["url_promocion"]
            this_cuenta = object["cuenta_promocion"]
            update.message.reply_text(
                "*{}:*\n\n{}\n\n*Más info en*: {}\n\n".format(
                    this_nombre, this_descripcion, this_url
                ),parse_mode=ParseMode.MARKDOWN,
            )
            print(this_nombre, this_descripcion, this_cuenta, "\n")
    VolverAlMenu(update, context)


# Consumo del Endpoint de promociones y match de datos
def datosIngresados(update, context):
    datos_usuario = context.user_data["datos_usuario"]
    cui = datos_usuario["CUI"]
    correo = datos_usuario["correo"]
    endpoint = "http://127.0.0.1:5000/usuarios/%s" % cui
    response = requests.get(endpoint)
    if response.status_code == 200:
        respuesta = response.json()
        this_correo = respuesta["correo"]
        this_cui = respuesta["cui"]
        this_nombre = respuesta["nombre"]
        this_codigo = respuesta["codigo_promocion"]
        print(correo, cui, this_correo, this_cui)
        if str(correo) == str(this_correo):

            update.message.reply_text(
                "Hola %s Hemos validado los siguientes datos:" % this_nombre
            )
            update.message.reply_text(
                "Nombre: {}\nCUI: {}\nCorreo Electronico: {}\nCodigo: {}".format(
                    this_nombre, this_cui, this_correo, this_codigo
                )
            )
            update.message.reply_text(
                "Se ha enviado un correo electronico a %s con tu codigo promocional:" % this_correo
            )

            """
            Envio de Email:
            """
            correo_user = 'support@wolvisor.com'
            password = 'contradebeiraca'
            subject = 'Cerveza Tona: Tu codigo promocional'
            
            body =  '\nHola: {}! Estos son tus datos registrados en nuestro sistema:\nCUI: {}\nCorreo Electronico: {}\nCodigo: {}'.format(
                    this_nombre, this_cui, this_correo, this_codigo)
            sent_from = correo_user
            to = [this_correo]
        
            email_text = 'Subject: {}\n\n{}'.format(subject, body)
            try:
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.ehlo()
                smtp_server.login(correo_user, password)
                smtp_server.sendmail(sent_from, to, email_text)
                smtp_server.close()
                print ("Email sent successfully!")
            except Exception as ex:
                print ("Something went wrong….",ex)




        else:
            update.message.reply_text(
                "El CUI {} y/o correo {} no estan asociados".format(cui, correo)
            )
    else:
        update.message.reply_text(
            "El CUI %s no esta registrado en la base de datos" % cui
        )
    datos_usuario["CUI"] = None
    datos_usuario["CUI"] = None
    VolverAlMenu(update, context)


def verificar_codigo(update: Update, context: CallbackContext) -> None:
    estado = context.user_data["estado"]
    if estado == "Pregunta:CUI":
        update.message.reply_text("Ingresa tu CUI:")
        context.user_data["estado"] = "Respuesta:CUI"
        echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
        updater.dispatcher.add_handler(echo_handler)

    elif estado == "Done":
        context.user_data["estado"] = "Menu:Promociones"

# Funcion central
def echo(update, context):
    estado = context.user_data["estado"]
    print(estado)
    datos_usuario = context.user_data["datos_usuario"]
    opcion = update.message.text
    if estado == "Respuesta:CUI":
        if datos_usuario["CUI"] != None:
            context.user_data["estado"] = "Respuesta:CUI"
            CommandHandler("verificar", verificar_codigo)

        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="El CUI ingresado es: " + update.message.text,
            )
            datos_usuario["CUI"] = update.message.text
            context.user_data["estado"] = "Respuesta:correo"
            update.message.reply_text("Ingresa tu Correo:")
            CommandHandler("verificar", verificar_codigo)
    elif estado == "Respuesta:correo":
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="El Correo ingresado es: " + update.message.text,
        )
        datos_usuario["correo"] = update.message.text
        context.user_data["estado"] = "Menu:Promociones"
        datosIngresados(update, context)

    elif estado == "Menu:Inicial":
        try:
            if opcion == "stickers":
                stickers(update, context)
            elif opcion == "fondos":
                fondos(update, context)
            elif opcion == "musica":
                audio(update, context)
            elif opcion == "promociones":
                MenuPromociones(update, context)
            else:
                opcion = int(opcion)
                if opcion < 0 or opcion > 4:
                    context.bot.send_message(
                        cht_id=update.effective_chat.id,
                        text="El Numero ingresado "
                        + update.message.text
                        + " No forma parte del menu, elija otra vez.",
                    )
                    start(update, context)
                else:
                    if opcion == 0:
                        start(update, context)
                    elif opcion == 1:
                        stickers(update, context)
                    elif opcion == 2:
                        fondos(update, context)
                    elif opcion == 3:
                        audio(update, context)
                    elif opcion == 4:
                        context.user_data["estado"] = "Menu:Promociones"
                        MenuPromociones(update, context)
                    print("Escogio", opcion)
        except:
            update.message.reply_text("Opcion no valida, elija otra vez.")
            start(update, context)
    elif estado == "Menu:Promociones":
        try:
            opcion = int(opcion)
            if opcion < 0 or opcion > 5:
                context.bot.send_message(
                    cht_id=update.effective_chat.id,
                    text="El Numero ingresado "
                    + update.message.text
                    + " No forma parte del menu, elija otra vez.",
                )
                MenuPromociones(update, context)
            else:

                if opcion == 0:
                    start(update, context)
                elif opcion == 1:
                    datosPromociones(update, context, "Toña")
                elif opcion == 2:
                    datosPromociones(update, context, "Victoria")
                elif opcion == 3:
                    context.user_data["estado"] = "Pregunta:CUI"
                    verificar_codigo(update, context)
                elif opcion == 4:
                    context.user_data["estado"] = "Pregunta:CUI"
                    verificar_codigo(update, context)
                elif opcion == 5:
                    MenuPromociones(update, context)
                print("Escogio", opcion)
        except:
            update.message.reply_text("Opcion no valida, por favor elija otra vez.")
            MenuPromociones(update, context)


# Inicio y disparador del bot
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
updater.idle()
