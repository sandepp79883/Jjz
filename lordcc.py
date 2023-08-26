import re
import asyncio
import requests
from telethon import TelegramClient, events

# Replace with your own values from https://my.telegram.org
api_id = 28370649
api_hash = '455ca8e2b7e8894285a90da368a73a4d'
channels = ['xforce_group8', 'teamnastyscr', 'ScrapperLala', 'BINEROS_CCS2',
            'LalaScrapperPublic', 'BINEROS_CCS02', 'Cc_Cheaker_Private',
            'Good_Charged_CCS', 'atlant1is', 'STRIPEC', 'aNamakaProof',
            'CRKSOO_CC7', 'VIPxPRINCE_IGCC', 'tedchk', 'StarterChannel',
            'liveccbinss', 'binsschat', 'xenscrape', 'ONLY_FARES']

# Your own channel username where you want to post the collected data
your_channel_username = 'L30RDCC'

# Initialize the TelegramClient with a custom session name
client = TelegramClient('my_session', api_id, api_hash)

# Dictionary to store the last message IDs for each channel
last_message_ids = {channel: None for channel in channels}

# Function to get credit card details from the API
def get_credit_card_details(cc_number):
    url = f'https://lookup.binlist.net/{cc_number}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

posted_cc_numbers = set()  # Set to store already posted credit card numbers

manual_entry = input("Enter manual entry text: ")

@client.on(events.NewMessage(chats=channels))
async def my_event_handler(event):
    print("Received a new message in channel:", event.chat.username)

    # Check if the message ID is different from the last known message ID for the channel
    if last_message_ids.get(event.chat.username) != event.id:
        # Save the new message ID
        last_message_ids[event.chat.username] = event.id

        # Use regex to find credit card numbers of the format "34225852467417585|08|2027|692"
        matches = re.findall(r'\b\d{16}\|\d{2}\|\d{4}\|\d{3}\b', event.raw_text)

        print("Found credit card matches:", matches)

        # If there are matches, post the details along with each credit card number to your own channel
        if matches:
            for cc_number in matches:
                # Check if the credit card number is already posted
                if cc_number in posted_cc_numbers:
                    # Delete the duplicate message
                    await event.delete()
                    continue

                cc_details = get_credit_card_details(cc_number)
                if cc_details:
                    # Construct the output message with custom formatting
                    output_message = (
                        f"✅ **L30RD SCRAP CC** **---------×----------×-----------×----------×------------**\n"
                        f"Card » `{cc_number}`\n"
                        f"Brand » `{cc_details.get('scheme', 'N/A')}`\n"
                        f"Bank » `{cc_details.get('bank', {}).get('name', 'N/A')}`\n"
                        f"Country » `{cc_details.get('country', {}).get('name', 'N/A')}`\n"
                        f"Type » `{cc_details.get('type', 'N/A')}`\n"
                        f"**---------×----------×-----------×----------×------------**\n"
                        "L30RD SCRAPPING CC BY @L30RD"
                    )

                    print("Posting message to channel:", your_channel_username)
                    # Post the output message to your own channel
                    await client.send_message(your_channel_username, output_message, parse_mode='md')

                    # Add the credit card number to the set of posted numbers
                    posted_cc_numbers.add(cc_number)

async def main():
    # Start the client and run it until disconnected
    await client.start()

    # Check if the client is logged in
    if await client.is_user_authorized():
        print("Telegram account is logged in.")
    else:
        print("Telegram account is NOT logged in.")

    # Check the connection status
    if client.is_connected():
        print("Telegram client is connected to the Telegram servers.")
    else:
        print("Telegram client is NOT connected to the Telegram servers.")

    await client.run_until_disconnected()

if __name__ == "__main__":
    # Run the event handler in a separate task
    client.loop.run_until_complete(main())
    client.loop.create_task(my_event_handler())
    client.loop.run_forever()
