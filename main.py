from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import token,botusername
from Functions import WriteData, ReadData, SendMessage

TOKEN: Final = token
BOT_USERNAME: Final = botusername

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
        
        if last_command == 'register' and data['organisationname'] in existingdata['organisations']:
            WriteData(data)
            return f"Congratulations! you have successfully registered in {processed} organisation, You can now send and receive anonymous broadcast messages"
        
        if last_command == 'register' and data['organisationname'] not in existingdata['organisations']:
            return f"Sorry! your organisation {data['organisationname']} is not registered with anonymous broadcaster, Either join existing organisations or create your own"

        if last_command == 'sendmessage' and data['organisationname'] in existingdata['organisations']:
            users = existingdata['users']
            for user in users:
                if data['chat_id'] ==  user['chat_id']:
                    continue
                chat_ids.append(user.get('chat_id'))
            SendMessage(chat_ids, processed )     
            return f"Your message has been successfully broadcasted anonymously"  

        if last_command == 'sendmessage' and data['organisationname'] not in existingdata['organisations']:
            return f"Sorry! you are not linked with any organisation to broadcast this message this message"    
        return processed
    else:
        return f"Sorry Some Issue"   

# Message Handler
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
