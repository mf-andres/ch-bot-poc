from typing import List

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

    url = f"https://api.telegram.org/bot{settings.telegram_token}/sendMessage"
    json_ = {
        "chat_id": "506901938",
        "text": message
    }
    requests.post(
        url=url,
        json=json_,
    )


@app.command()
def wikipedia():
    # get info
    # send message
    pass


if __name__ == '__main__':
    app()
