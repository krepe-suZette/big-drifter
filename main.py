import logging
import time

import watchman
import alert_telegram
import alert_discord


formatter = logging.Formatter('%(asctime)s|%(message)s')

logger = logging.getLogger("log")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('detect.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def main():
    # 감시 예정 queue를 불러와서 확인 -> 처형명단에 있는 유저들 텔그로 -> 감시 queue에 추가
    # 75: GambitPrime
    execution_list = watchman.check_from_queue(75)
    for data in execution_list:
        # [활동 시작 시간(GMT), instance_id, fireteam, [display_name, clan_name], mode, stats]
        logger.info(f"{data[3][0]}|{data[3][1]}|{data[4]}|{data[1]}")
        # 4인큐+ 잠수 건너뛰기
        if data[2] >= 4:
            continue
        alert_telegram.send_to_channel(data, "@bigdrifter")
        alert_discord.send_webhook(data)
    queue = watchman.add_members_to_queue("레이너특공대", 75)
    return


if __name__ == "__main__":
    main()
