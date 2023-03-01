# IMPORT MODULES
import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv


# CALL DOTENV TO LOAD ENV VARS
load_dotenv()

print("Starting...")

# BASIC ENV VARS
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
FROM = os.getenv("FROM")
TO = os.getenv("TO")
ERROR_CONTACT = os.getenv("ERROR_CONTACT")

# INITIALIZE CLIENT
try:
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    client.start()

except Exception as error:
    print(f"ERROR - {error}")
    exit(1)


# create a function to remove words with hashtags infront of them in the message
def remove_hashtags(text):
    words = text.split()

    new_words = []
    for word in words:
        if not word.startswith("#"):
            new_words.append(word)

    return " ".join(new_words)


# REMOVE LINKS FROM MESSAGES
def remove_links(message):
    # regular expression pattern to match URLs
    url_pattern = r"(https?://\S+)"
    urls = re.findall(url_pattern, message)

    for url in urls:
        if "tradingview" not  in url:
            print("ten")
        else:
             message = "falise"
    return message

# MESSAGE HANDLER
@client.on(events.NewMessage(chats=FROM))
async def handler(event):
    message = event.message.message
    no_hashtag_message = ""
    no_links_message = ""
    if event.media.__class__.__name__ != "MessageMediaPoll":
        if "#" in message:
            no_hashtag_message += remove_hashtags(message)
        else:
            no_hashtag_message += message
        no_links_message += remove_links(no_hashtag_message)

        try:
            if event.media:
                
                await client.download_media(event.message, file="temp.jpg")
                await client.send_file(TO, "temp.jpg", caption=no_links_message)
                os.remove("temp.jpg")
              
            else:
                if no_links_message:
                    if "falise" not in no_links_message:
                        await client.send_message(TO, no_links_message)
            print("sent")
        except Exception as error:
            await client.send_message(
                ERROR_CONTACT,
                f"ALERT, AN ERROR OCCURED IN THE BOT.\n ERROR - {error}\n MESSAGE - {event.message.message} ",
            )
            print(f"ERROR - {error}")


print("Bot has started.")

# RUN CLIENT
client.run_until_disconnected()