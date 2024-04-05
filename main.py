from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import token
import json
import requests

def ReadData():
    try:
        with open('data.json', 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = {} 
    return existing_data 

def SendMessage(chat_ids, message):
    for id in chat_ids:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={message}"
        print(requests.get(url).json())   

def WriteData(data, org=None):
    existing_data = ReadData()

    if org is not None:
        if data not in existing_data['organisations']:
            existing_data['organisations'].append(data)
        else:
            print(f"Organisation {data} already exists.")
    else:
        if data not in existing_data['users']:
            existing_data['users'].append(data)
        else:
            print(f"User {data} already exists.")

    # Writing the updated data back to the JSON file
    with open('data.json', 'w') as json_file:
        json.dump(existing_data, json_file)


TOKEN: Final = token
BOT_USERNAME: Final = "@Anonymous_Broadcaster_Bot"

last_command = None
# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thankyou for Visiting Anonymous Broadcaster, YOUR VOICE IN YOUR ORGANISATION \nUse Menu to Register Yourself in Broadcaster List or to Send Anonymous Message to your Organisation\nOr you can create your own organisation and invite your teammates")

async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_command
    last_command = 'register'
    await update.message.reply_text("Please Enter your Organisation Name")

async def sendmesssage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_command
    last_command = 'sendmessage'
    await update.message.reply_text("Please Enter your message to Broadcast Anonymously in your Organisation")

async def create_organisation_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_command
    last_command = 'createorganisation'
    await update.message.reply_text("Please Enter your Organisation Name")


# Response

def handle_response(text:str, data:dict) -> str:
    existingdata = ReadData()
    processed: str = text.lower()

    if data is not None:
        print("Data", data)
        if last_command == 'createorganisation' and data['organisationname'] not in existingdata['organisations']:
            WriteData(data['organisationname'], True)
            WriteData(data)
            return f"Congratulations! organisation {processed} successfully registered with Anonymous Broadcaster, You can now ask your teammates to join the organisation"
        
        if last_command == 'createorganisation' and data['organisationname'] in existingdata['organisations']:
            return f"Sorry! Organisation {processed} already registered with Anonymous Broadcaster, Join the existing one or create different organisation"        
        
        if last_command == 'register' and data['organisationname'] in existingdata['organisations']: # Check in Database if Organisation Exists
            WriteData(data)
            return f"Congratulations! you have successfully registered in {processed} organisation, You can now send and receive anonymous broadcast messages"
        
        if last_command == 'register' and data['organisationname'] not in existingdata['organisations']: # Check in Database if Organisation Exists
            return f"Sorry! your organisation {data['organisationname']} is not registered with anonymous broadcaster, Either join existing organisations or create your own"

        if last_command == 'sendmessage' and data['organisationname'] in existingdata['organisations']: # Check if user has right to broadcast message in the organisation
            # Send Last message to everyone in the organisation except the sender
            chat_ids = []
            users = existingdata['users']
            for user in users:
                if data['chat_id'] ==  user['chat_id']:
                    continue
                chat_ids.append(user.get('chat_id'))
            SendMessage(chat_ids, processed )     
            return f"Your message has been successfully broadcasted anonymously"  

        if last_command == 'sendmessage' and data['organisationname'] not in existingdata['organisations']: # Check if user has right to broadcast message in the organisation
            return f"Sorry! you are not linked with any organisation to broadcast this message this message"    
        return processed
    else:
        return f"Sorry Some Issue"   

async def handle_message(update: Update, context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text:str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    try:   
        if last_command == "createorganisation":
            data = {
                "username": update.message.from_user.username,
                "chat_id": update.message.chat.id,
                "organisationname": text.lower()
            }
            response: str = handle_response(text, data)

        if last_command == "register":
            data = {
                "username": update.message.from_user.username,
                "chat_id": update.message.chat.id,
                "organisationname": text.lower()
            }
            response: str = handle_response(text, data)

        if last_command == "sendmessage":
            existingdata = ReadData()
            organisationname = None 
            for i in existingdata['users']:
                if i['chat_id'] == update.message.chat.id:
                    print("Done:", update.message.chat.id, "Done: ", i['chat_id'])
                    organisationname = i['organisationname']
                    break

            data = {
                "username": update.message.from_user.username,
                "chat_id": update.message.chat.id,
                "organisationname": organisationname,
                "message": text.lower()
            }

            response: str = handle_response(text, data)



        # print("Bot:", response)
        await update.message.reply_text(response)
    except  Exception as e:
        response: str = handle_response(text, None)
        await update.message.reply_text(response)


if __name__ == '__main__':
    print("Starting Bot...")

    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('register', register_command))
    app.add_handler(CommandHandler('sendmessage', sendmesssage_command))
    app.add_handler(CommandHandler('createorganisation', create_organisation_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Polling...")
    app.run_polling(poll_interval=3)
