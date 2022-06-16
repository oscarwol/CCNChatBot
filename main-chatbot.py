"""
- NPL ChatBot: Cerveceria Nicaraguence (Promociones & Comunicacion Continua)
- Version: 1.0
- Created for: WOL Media & Digital Division (soportedev@wol.group)
- License: Wol Media Copyrighted Software
- Author: Oscar E. Morales (oscarmoralesgt.com)

- Rights reserved, This program and code is issued for the purposes that the interested party deems appropriate.
"""

# Importamos las librerias y paquetes necesarios
from datetime import datetime 
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

if __name__ == "__main__":
    #5337008655:AAHVFTKS_YOKeUhi4LpbLyDOr5C2t5PJP6I
    updater = Updater("5337008655:AAHVFTKS_YOKeUhi4LpbLyDOr5C2t5PJP6I")
    reply_keyboard = [["stickers", "fondos"], ["musica", "promociones"]]
    promo_keyboard = [["1", "2"], ["3", "4"]]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    markup_promo = ReplyKeyboardMarkup(promo_keyboard, one_time_keyboard=True)

    #Funcion para saber si el usuario tiene una sesión activa con el bot
    def user_has_data(update, context):
        return bool(context.user_data)

    # Funcion de Inicio (Disparador / Trigger)
    def start(update: Update, context: CallbackContext) -> None:
        context.user_data["estado"] = "Menu:Inicial"
        context.user_data["datos_usuario"] = {"CUI": None, "correo": None, "Pais": None}
        welcomeMessage(update,context)
        menuInicial(update, context)
        seleccion_por_numero(update, context)

    def welcomeMessage(update, context):
        nombre_de_usuario = update.message.from_user.first_name
        update.message.reply_text(
            "¡Hola *{}*! Gracias por comunicarte con el soporte automatizado de *Cerveza Toña*".format(
                nombre_de_usuario),
                parse_mode=ParseMode.MARKDOWN,
        )


    # Funcion que nos permite seleccion por numero en los diferentes menus
    def seleccion_por_numero(update, context):
        echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
        updater.dispatcher.add_handler(echo_handler)

    """
    Menus y Opciones disponibles dentro del chat
    """

    def menuInicial(update, context):
        update.message.reply_text(
            "Escribe 1️⃣ o *stickers* para obtener los mejores stickers de Cerveza Toña",
            parse_mode=ParseMode.MARKDOWN,
        )
        update.message.reply_text(
            "Escribe 2️⃣ o *fondos* para obtener los mejores Fondos de pantalla de Cerveza Toña",
            parse_mode=ParseMode.MARKDOWN,
        )
        update.message.reply_text(
            "Escribe 3️⃣ o *música* para obtener las mejores canciones de Cerveza Toña",
            parse_mode=ParseMode.MARKDOWN,
        )
        update.message.reply_text(
            "Escribe 4️⃣ o *promociones* para ver las promociones existentes o verificar tu código promocional",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=markup,
        )

    def menu_Promociones(update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            "Escribe 1️⃣ para ver las promociones válidas para Nicaragua",
            parse_mode=ParseMode.MARKDOWN,
        )
        update.message.reply_text(
            "Escribe 2️⃣ para verificar tu código de canje - Promo Toña Light 🇳🇮​",
            parse_mode=ParseMode.MARKDOWN,
        )
        update.message.reply_text(
            "Escribe 3️⃣ para ver las promociones válidas para Panamá",
            parse_mode=ParseMode.MARKDOWN,
        )
        update.message.reply_text(
            "Escribe 4️⃣ para verificar tu código de canje - Promo Toña Light 🇵🇦",
            parse_mode=ParseMode.MARKDOWN,
        )                
        update.message.reply_text("Escribe 0️⃣ para regresar al menú inicial")

        context.user_data["estado"] = "Menu:Promociones"
        context.user_data["datos_usuario"] = {"CUI": None, "correo": None, "Pais": None}

        seleccion_por_numero(update, context)

    def VolverAlMenu(update, context):
        if context.user_data["estado"] == "Menu:Inicial":
            update.message.reply_text(
                "Escribe 0️⃣ para mostar el menu nuevamente, o elige una de las opciones anteriores"
            )
        elif context.user_data["estado"] == "Menu:Promociones":
            update.message.reply_text(
                "Escribe 5️⃣ para regresar al Menu de Promociones \nEscribe 0️⃣ para regresar al menu inicial\n"
            )
        seleccion_por_numero(update, context)

    """
    Envio de materiales multimedia
    """
    
    def stickers(update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            "Aqui tienes los stickers promocionales de la temporada ¡Que los disfrutes!"
        )
        lss = Sticker(
            "CAACAgEAAxkBAAEE0jhijokXteL04gMLk7E7O2Of_B81-QACjAIAArvqwUXgFP4Q_Tb3biQE",
            "5026556748001968780",
            500,
            500,
            False,
            False,
        )
        update.message.reply_sticker(lss)
        update.message.reply_text(
            "Haz tap en el sticker para obtener todos los stickers de Cerveza Toña!"
        )
        VolverAlMenu(update, context)

    def fondos(update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            "Aqui tienes los fondos promocionales de la temporada ¡Que los disfrutes!"
        )
        update.message.reply_photo(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/fondo1.jpg"
        )
        update.message.reply_photo(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/fondo2.jpg"
        )
        update.message.reply_photo(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/fondo3.jpg"
        )
        update.message.reply_photo(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/fondo4.jpg"
        )
        update.message.reply_photo(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/fondo5.png"
        )
        update.message.reply_photo(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/fondo6.png"
        )
        VolverAlMenu(update, context)

    def audio(update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            "Aqui tienes las canciones promocionales de la temporada ¡Que los disfrutes!"
        )
        update.message.reply_audio(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/Ay%2C%20que%20linda%20es%20nicaragua.mp3"
        )
        update.message.reply_audio(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/Encuentro.mp3"
        )
        update.message.reply_audio(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/Festival%20cervecero.mp3"
        )
        update.message.reply_audio(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/Hecha%20de%20nicaragua.mp3"
        )
        update.message.reply_audio(
            "https://raw.githubusercontent.com/oscarwol/CCNChatBot/main/sources/Tienes%20ese%20no%20se%20que.mp3"
        )
        VolverAlMenu(update, context)

    """
    Seccion de Promociones y verificación de códigos Promocionaels:

    """


    # Consumo del Endpoint de promociones y match de datos
    def comprobar_promociones(update, context, data):
        if bool(data['pais']):
            endpoint = "https://apiswolgroup.com/chatbot/promociones?pais=%s" % data['pais']
            response = requests.get(endpoint)
            if response.status_code == 200:
                respuesta = response.json()
                update.message.reply_text(
                    "Este es el listado de las promociones activas para %s:" % data['pais']
                    )
                for object in respuesta:
                    titulo = object["titulo"]
                    descripcion = object["descripcion"]
                    url = object["url"]
                    url_terminos = object["url_terminos"]
                    fecha_de_inicio = object["fecha_inicio"][:10]
                    fecha_de_inicio = datetime.strptime(fecha_de_inicio, '%Y-%m-%d')
                    fecha_de_inicio_fixed =datetime.strftime(fecha_de_inicio, '%d/%m/%Y')
                    fecha_fin = object["fecha_fin"][:10]
                    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
                    fecha_de_fin_fixed = datetime.strftime(fecha_fin, '%d/%m/%Y')


                    update.message.reply_text(
                        "*{}:*\n\n{}\n\nInicia: {},\nFinaliza: {}\n\n*Para más información:* {}\n\n*Términos y condiciones*: {}\n\n".format(
                            titulo, descripcion, fecha_de_inicio_fixed, fecha_de_fin_fixed, url, url_terminos,),parse_mode=ParseMode.MARKDOWN,
                    )
            if response.status_code == 404:
                update.message.reply_text((
                    "No hay promociones vigentes en este momento ¡Vuelve más tarde!"
                    ))
        else:
            update.message.reply_text((
                    "No hay promociones disponibles para este país"
                    )
                )
        VolverAlMenu(update, context)


    # Consumo del Endpoint de promociones y match de datos
    def datosIngresados(update, context):
        datos_usuario = context.user_data["datos_usuario"]
        cui = str(datos_usuario["CUI"]).upper()
        pais = datos_usuario["Pais"]

        correo = str(datos_usuario["correo"]).upper()
        if pais == "Nicaragua":
            endpoint = "https://apiswolgroup.com/chatbot/usuarios/nicaragua/%s" % cui
        else:
            endpoint = "https://apiswolgroup.com/chatbot/usuarios/panama/%s" % cui
        response = requests.get(endpoint)
        if response.status_code == 200:
            respuesta = response.json()
            this_correo = str(respuesta["email"]).upper()
            this_cui = str(respuesta["cui"]).upper()
            this_nombre = respuesta["nombre"]
            this_codigo = respuesta["codigo"]
            if str(correo) == str(this_correo):

                update.message.reply_text(
                    "Hola %s Hemos validado los siguientes datos:" % this_nombre
                )
                update.message.reply_text(
                    "Nombre: {}\nCédula: {}\nCorreo Electronico: {}\nCódigo: {}\nPais: {}".format(
                        this_nombre, this_cui, this_correo, this_codigo, pais
                    )
                )
                update.message.reply_text(
                    "Se ha enviado un correo electrónico a %s con tu código promocional:"
                    % this_correo
                )

                """
                Envio de Email:
                """
                correo_user = "support@wolvisor.com"
                password = "mmtcpyqsilnsgigs"
                subject = "Cerveza Tona: Tu código promocional"

                body = "\nHola: {}! Estos son tus datos registrados en nuestro sistema:\nCédula: {}\nCorreo Electrónico: {}\nCódigo: {}\nPaís: {}".format(
                    this_nombre, this_cui, this_correo, this_codigo, pais
                )
                sent_from = correo_user
                to = [this_correo]

                email_text = "Subject: {}\n\n{}".format(subject, body)
                try:
                    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                    smtp_server.ehlo()
                    smtp_server.login(correo_user, password)
                    smtp_server.sendmail(sent_from, to, email_text)
                    smtp_server.close()
                    print("Email sent successfully!")
                except Exception as ex:
                    print("Something went wrong….", ex)

            else:
                update.message.reply_text(
                    "La Cédula {} y/o correo {} no estan asociados".format(cui, correo)
                )
        else:
            update.message.reply_text(
                "La Cédula %s no esta registrada en la base de datos" % cui
            )
        datos_usuario["CUI"] = None
        datos_usuario["Pais"] = None
        VolverAlMenu(update, context)

    def verificar_codigo(update: Update, context: CallbackContext) -> None:
        estado = context.user_data["estado"]
        if estado == "Pregunta:CUI":
            update.message.reply_text("Por favor, ingresa tu Cédula o número de indentificación:")
            context.user_data["estado"] = "Respuesta:CUI"
            echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
            updater.dispatcher.add_handler(echo_handler)

        elif estado == "Done":
            context.user_data["estado"] = "Menu:Promociones"

    # Funcion central
    def echo(update, context):
        if user_has_data(update,context):
            estado = context.user_data["estado"]
            datos_usuario = context.user_data["datos_usuario"]
            opcion = update.message.text
            if estado == "Respuesta:CUI":
                if datos_usuario["CUI"] != None:
                    context.user_data["estado"] = "Respuesta:CUI"
                    CommandHandler("verificar", verificar_codigo)

                else:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="La Cédula ingresada es: " + update.message.text,
                    )
                    datos_usuario["CUI"] = update.message.text
                    context.user_data["estado"] = "Respuesta:correo"
                    update.message.reply_text("Ahora, ingresa tu Correo electronico (email):")
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
                        context.user_data["estado"] = "Menu:Promociones"
                        menu_Promociones(update, context)
                        # update.message.reply_text("Opcion Deshabilitada temporalmente, disculpe las molestias.")
                        # MenuInicial(update, context)
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
                                menu_Promociones(update, context)
                                # update.message.reply_text("Opcion Deshabilitada temporalmente, disculpe las molestias.")
                                # MenuInicial(update, context)
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
                        menu_Promociones(update, context)
                    else:

                        if opcion == 0:
                            start(update, context)
                        elif opcion == 1:
                            comprobar_promociones(update, context, {"pais": "Nicaragua"})
                        elif opcion == 2:
                            datos_usuario['Pais'] = "Nicaragua"
                            context.user_data["estado"] = "Pregunta:CUI"
                            verificar_codigo(update, context)
                        elif opcion == 3:
                            comprobar_promociones(update, context, {"pais": "Panama"})
                        elif opcion == 4:
                            context.user_data["estado"] = "Pregunta:CUI"
                            datos_usuario['Pais'] = "Panama"
                            verificar_codigo(update, context)
                        elif opcion == 5:
                            menu_Promociones(update, context)
                except:
                    update.message.reply_text(
                        "Opcion no valida, por favor elija otra vez."
                    )
                    menu_Promociones(update, context)
        else:
            start(update, context)

    # Inicio y disparador del bot

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    updater.dispatcher.add_handler(echo_handler)
    updater.dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()
