import telegram
from telegram import Bot
import datetime

from bungie_api import DestinyActivityModeType

with open("TELEGRAM_TOKEN", "r") as f:
    TOKEN = f.read().strip()
# https://t.me/bigdrifter
CHAT_ID = "@bigdrifter"
bot = Bot(token=TOKEN)


def send_to_channel(data, chat_id=CHAT_ID):
    # TODO msg_md도 전역으로 빼던지 해서 코드 깔끔하게
    # [활동 시작 시간(GMT), instance_id, fireteam, [display_name, clan_name], mode, stats]
    msg_md = f"""*잠수 감지!*

{data[3][0]} - {data[3][1]}
KST {datetime.datetime.strptime(data[0], "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=9)}
활동명: {DestinyActivityModeType.get(data[4], data[4])}
KDA: {data[5]["kills"]:0.0f}/{data[5]["deaths"]:0.0f}/{data[5]["assists"]:0.0f}
점수(티끌): {data[5]["score"]:0.0f}
화력팀원: {data[2]}명

Link: [DestinyTracker](https://destinytracker.com/d2/pgcr/{data[1]})"""
    result = bot.send_message(chat_id=CHAT_ID, text=msg_md, parse_mode=telegram.ParseMode.MARKDOWN)
    return result


if __name__ == "__main__":
    res = bot.send_message(chat_id=CHAT_ID, text="hello Python world")
    print(res)
