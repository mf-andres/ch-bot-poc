from typing import List
from urllib import parse

import pyleague
import requests
import typer

from chuinibot.infrastructure.path_utils import get_project_root_path
from chuinibot.infrastructure.settings import Settings

app = typer.Typer()
settings = Settings(_env_file=get_project_root_path() / '.env', _env_file_encoding='utf-8')


@app.command()
def league_set_participants(participants: List[str]):
    pyleague.do_init(participants)


@app.command()
def league_send_day():
    # TODO change paricipants from telegram
    # get info
    day_pointer, group_pairs = pyleague.set_next_day()

    # send message
    message = f"Day {day_pointer[0]}\n"
    for pair in group_pairs:
        message += f"{pair[0]} VS {pair[1]}\n"

    send_to_telegram(message)
    send_to_rocketchat(message)


def send_to_telegram(message: str):
    url = f"https://api.telegram.org/bot{settings.telegram_token}/sendMessage"
    json_ = {
        "chat_id": "506901938",
        "text": message
    }
    requests.post(
        url=url,
        json=json_,
    )


def send_to_rocketchat(message):
    # Set the URL
    url = "https://rocketchat.gradiant.org/api/v1/chat.postMessage"

    # Set the payload
    group_id = "8xwk9gMLK5ufLsDDk"
    payload = {
        "channel": group_id,
        "text": message
    }

    # Set the headers
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": settings.rocketchat_token,
        "X-User-Id": "4AB8ptpQhgxoMdDmo"
    }

    # Send the POST request to the Rocket Chat API
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code)


@app.command()
def send_random_wikipedia_articles():
    links = get_links_from_wikipedia()
    message = "Wikipedia Links:\n\n"
    for i, link in enumerate(links):
        message += f"{i} - {link}\n"
    send_to_telegram(message)


def get_links_from_wikipedia():
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": 5,  # Number of random pages to retrieve
        "rnnamespace": 0,  # Only retrieve pages in the main namespace
    }
    # Send the request to the API and retrieve the response
    response = requests.get(url, params=params)
    # Parse the JSON data and extract the page titles
    data = response.json()
    pages = data["query"]["random"]
    # Print the page titles and links
    links = list()
    for page in pages:
        title = page["title"]
        title = parse.quote(title)
        link = f"https://en.wikipedia.org/wiki/{title}"
        links.append(link)
        print(f"{title}: {link}")
    return links


if __name__ == '__main__':
    app()
