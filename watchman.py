import json
import datetime
import telegram

import bungie_api


def get_fireteam_count_from_pgcr(instance_id, fireteam_id) -> int:
    pgcr = bungie_api.get_post_game_carnage_report(instance_id)
    fireteam = sum(1 for i in pgcr["entries"] if i["values"]["fireteamId"]["basic"]["value"] == fireteam_id)
    return fireteam


def check_from_queue(mode=75) -> [[datetime.datetime, str, int, [str, str], dict], ...]:
    # TODO 값 반환 깔끔하게 정리
    """[활동 시작 시간(GMT), instance_id, fireteam, [display_name, clan_name], mode, stats]
    """
    with open("queue.json", "r", encoding="utf-8") as f:
        queue = json.load(f)
    with open("checked.json", "r") as f:
        checked = json.load(f)
    new_checked = []
    results = []

    for checklist in queue:
        membership_id, membership_type, character_id, *user_info = checklist
        activity = bungie_api.get_activity_history(membership_type, membership_id, character_id, count=1, mode=mode).get("activities", [{}])[0]
        if not activity:
            continue
        instance_id = activity["activityDetails"]["instanceId"]
        new_checked.append(instance_id)
        if instance_id in checked:
            continue
        stats = {x: y["basic"]["value"] for x, y in activity["values"].items()}
        if stats["completed"] and stats["kills"] < 2 and stats["score"] == 0:
            fireteam = get_fireteam_count_from_pgcr(instance_id, stats["fireteamId"])
        # 인원수와 무관하게 잠수기록을 result에 추가
        results.append([datetime.datetime.strptime(activity["period"], "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=9), instance_id, fireteam, user_info, mode, stats])
    with open("checked.json", "w") as f:
        json.dump(new_checked, f)
    return results


def add_members_to_queue(clan_name: str, mode=75) -> None:
    members = bungie_api.get_online_clan_members(clan_name)
    queue = []
    for member in members:
        display_name = member["destinyUserInfo"]["displayName"]
        membership_id = member.get("destinyUserInfo", {}).get("membershipId")
        membership_type = member.get("destinyUserInfo", {}).get("membershipType")
        profile = bungie_api.get_profile(membership_type, membership_id, [204])
        if not profile.get("characterActivities", {}).get("data"):
            continue
        chars = [(y["dateActivityStarted"], x) for x, y in profile["characterActivities"]["data"].items()]
        last_char = sorted(chars)[-1][1]    # last played character's character_id
        mode_type = profile["characterActivities"]["data"][last_char].get('currentActivityModeType', -1)
        if mode_type == mode:
            # membership_id, membership_type, character_id
            queue.append([membership_id, membership_type, last_char, display_name, clan_name])
    with open("queue.json", "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False)
    return queue


def main():
    queue = add_members_to_queue("레이너특공대", 48)
    execution_list = check_from_queue(48)
    return


if __name__ == "__main__":
    main()
