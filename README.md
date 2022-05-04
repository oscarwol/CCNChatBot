# CCNChatBot
Chatbot de CCN

# CCN NPL ChatBot: 

NPL ChatBot: Cerveceria Nicaraguence (Promociones, comunicacion continua & atención al cliente)

Version 1.0; created for WOL Media & Digital Division (soportedev@wol.group)


## 🚀 Installation

Following the instructions:

```bash
pip install requirements.txt
```
    
## 💻 Instructions / How to use 

To run the script you need to configure first a Bot 
in Telegram, after you'll get a token

Put the token in the Updater method.

```python
updater = Updater("YOURTOKENHERE")
```

---

For the section of verification and promotions, you need to
configure some endpoints to consume the data

Promotions:
```python
def datosPromociones(update, context, tipo):
    endpoint = "http://127.0.0.1:5000/promos/%s" % tipo
```

Users for verification code:
```python
def datosIngresados(update, context):
    datos_usuario = context.user_data["datos_usuario"]
    cui = datos_usuario["CUI"]
    correo = datos_usuario["correo"]
    endpoint = "http://127.0.0.1:5000/usuarios/%s" % cui
```

NOTE: The variable 'datos_usuario' is a context.user_data

---

## 🗝 License


Rights reserved, this program and code is issued for the purposes that the interested party deems appropriate.


## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/ozk404)

[![portfolio](https://camo.githubusercontent.com/3c3250e8d4bf4fe0e1455b2aa88ef0b0f349e98d3a170a00d34802fac9f26f5d/68747470733a2f2f692e696d6775722e636f6d2f6a6a66777a787a2e6a7067)](https://www.oscarmoralesgt.com)
