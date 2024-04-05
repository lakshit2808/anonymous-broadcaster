# Anonymous Message Broadcaster

## Project Description
Anonymous Broadcaster is a Telegram bot designed to facilitate anonymous communication within organizations. Users can register themselves with the bot, join existing organizations, or create their own organizations. Once registered, users can send messages anonymously to their organization members.

### Feature:
User Registration: Users can register themselves with the bot by providing their organization name.
Organization Creation: Users can create new organizations.
Anonymous Messaging: Users can send messages anonymously within their organizations.
Feedback Handling: The bot handles user messages, registering users, creating organizations, and sending messages, providing appropriate feedback to users.

### Components:
Telegram Bot Framework: Utilizing the Telegram Bot API for communication.
Data Management: Functions for reading and writing data about organizations and users.
Message Handling: Logic for processing user messages and responding accordingly.
Command Handling: Commands for starting, registering, sending messages, and creating organizations.
Response Handling: Logic for generating appropriate responses based on user actions.

### Technical Details:
Language: Python
Dependencies: telegram, typing, config, Functions
Token Management: Utilizes a Telegram bot token for authentication and access.
Error Handling: Includes exception handling to manage errors gracefully.
Persistence: Utilizes data storage for maintaining information about organizations and users.

### Future Improvements:
Enhanced Security: Implement additional security measures to ensure anonymity.
User Authentication: Integrate user authentication mechanisms for better control.
Multiple Organisation Signup; User ability to communicate within multiple organisation
User Interface: Develop a user-friendly interface for easier interaction.
Scalability: Design the system to handle a larger user base and increased usage.

### Conclusion
Anonymous Broadcaster provides a platform for secure and anonymous communication within organizations, promoting transparency and open dialogue while preserving anonymity. With further enhancements and optimizations, it can become a valuable tool for various organizations seeking confidential communication channels.

## Installiation

 `pip3 install python-telegram-bot requests`

## Execution

`python3 main.py`

## Testing

- Search for Anonymous Broadcaster on Telegram and Select `@Anonymous_Broadcaster_Bot`

![alt text](/images/image.png)

- Click on Start
![alt text](/images/image-1.png)

- Click on Menu
![alt text](/images/image-2.png)

- Now Utilise the Bot by Either Creating or Joining the Organisation or you can send anonymous message to your organisation
![alt text](/images/image-3.png)
