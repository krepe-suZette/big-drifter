import requests
import json

from bungie_api import DestinyActivityModeType


with open("DISCORD_WEBHOOK", "r") as f:
    WEBHOOK_URL = f.read().strip()


def send_webhook(url, data):
    # [활동 시작 시간(GMT), instance_id, fireteam, [display_name, clan_name], mode, stats]
    message = {
        "username": "BIG DRIFTER(β)",
        "embeds": [
            {
                "author": {
                    "name": f"잠수 감지!!",
                },
                "description": (
                    f"자세한 정보는 [여기](https://destinytracker.com/d2/pgcr/{data[1]})를 참조해주세요."
                ),
                "fields": [
                    {
                        "name": "모드",
                        "value": f"{DestinyActivityModeType.get(data[4], data[4])} ",
                        "inline": True
                    },
                    {
                        "name": "이름",
                        "value": f"{data[3][0]}",
                        "inline": True
                    },
                    {
                        "name": "클랜",
                        "value": f"{data[3][1]}",
                        "inline": True
                    },
                    {
                        "name": "KDA",
                        "value": f"{data[5]['kills']:0.0f}/{data[5]['deaths']:0.0f}/{data[5]['assists']:0.0f}",
                        "inline": True
                    },
                    {
                        "name": "점수(티끌)",
                        "value": f"{data[5]['score']:0.0f}",
                        "inline": True
                    },
                    {
                        "name": "화력팀원",
                        "value": f"{data[2]}명",
                        "inline": True
                    },
                ],
                "color": 0x00ac00,
                "timestamp": data[0]
            }
        ]
    }
    result = requests.post(url, data=json.dumps(message), headers={"Content-Type": "application/json"})
    print(result)


if __name__ == "__main__":
    pass
