import os
import re
import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageEntityTextUrl
import pandas as pd
from colorama import Fore, Style
import details as ds

# Login details
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number

async def main():
    client = TelegramClient(phone, api_id, api_hash)

    await client.start()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter the code: '))

    print(f'{Fore.CYAN}Please enter a target Telegram channel (e.g. https://t.me/{Fore.LIGHTYELLOW_EX}your_channel{Fore.CYAN}):{Style.RESET_ALL}\n')
    print()

    while True:
        try:
            channel_name = input("Please enter a Telegram channel name: ")
            print(f'You entered "{channel_name}"')
            answer = input('Is this correct? (y/n) ')
            if answer == 'y':
                print(f'Scraping URLs from {channel_name}...')
                break
        except:
            continue

    urls = set()  # Use a set to deduplicate URLs

    async for message in client.iter_messages(channel_name):
        if message.entities is not None:
            for entity in message.entities:
                if isinstance(entity, MessageEntityTextUrl):
                    url = entity.url
                    if 'https://t.me/' in url:
                        match = re.match(r'https?://t\.me/([^/\s]+)/?', url)
                        if match:
                            channel_link = f'https://t.me/{match.group(1)}'
                            urls.add(channel_link)
                            print(f"URL - {Fore.CYAN}https://t.me/{match.group(1)}{Style.RESET_ALL}")
        else:
            if message.text and isinstance(message.text, str):
                regex = r'https?://t\.me/([^/\s]+)/?'
                matches = re.findall(regex, message.text)
                for match in matches:
                    channel_link = f'https://t.me/{match}'
                    urls.add(channel_link)
                    print(f"URL - {Fore.CYAN}https://t.me/{match}{Style.RESET_ALL}")

    urls_folder = 'URLs'
    os.makedirs(urls_folder, exist_ok=True)
    output_filename = os.path.join(urls_folder, f'{channel_name}.csv')

    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(urls))

    print(f'URLs scraped successfully. Saved to: {output_filename}')

if __name__ == '__main__':
    asyncio.run(main())
