import requests
import urllib
import datetime
import json


with open("API_KEY", "r") as f:
    HEADERS = {"X-API-KEY": f.read().strip()}

# http://destinydevs.github.io/BungieNetPlatform/docs/schemas/Destiny-HistoricalStats-Definitions-DestinyActivityModeType
DestinyActivityModeType = {
    -1: 'Orbit',
    0: 'none',
    2: 'Story',
    3: 'Strike',
    4: 'Raid',
    5: 'AllPvP',
    6: 'Patrol',
    7: 'AllPvE',
    9: 'Reserved9',
    10: 'Control',
    11: 'Reserved11',
    12: 'Clash',
    13: 'Reserved13',
    15: 'CrimsonDoubles',
    16: 'Nightfall',
    17: 'HeroicNightfall',
    18: 'AllStrikes',
    19: 'IronBanner',
    20: 'Reserved20',
    21: 'Reserved21',
    22: 'Reserved22',
    24: 'Reserved24',
    25: 'AllMayhem',
    26: 'Reserved26',
    27: 'Reserved27',
    28: 'Reserved28',
    29: 'Reserved29',
    30: 'Reserved30',
    31: 'Supremacy',
    32: 'PrivateMatchesAll',
    37: 'Survival',
    38: 'Countdown',
    39: 'TrialsOfTheNine',
    40: 'Social',
    41: 'TrialsCountdown',
    42: 'TrialsSurvival',
    43: 'IronBannerControl',
    44: 'IronBannerClash',
    45: 'IronBannerSupremacy',
    46: 'ScoredNightfall',
    47: 'ScoredHeroicNightfall',
    48: 'Rumble',
    49: 'AllDoubles',
    50: 'Doubles',
    51: 'PrivateMatchesClash',
    52: 'PrivateMatchesControl',
    53: 'PrivateMatchesSupremacy',
    54: 'PrivateMatchesCountdown',
    55: 'PrivateMatchesSurvival',
    56: 'PrivateMatchesMayhem',
    57: 'PrivateMatchesRumble',
    58: 'HeroicAdventure',
    59: 'Showdown',
    60: 'Lockdown',
    61: 'Scorched',
    62: 'ScorchedTeam',
    63: 'Gambit',
    64: 'AllPvECompetitive',
    65: 'Breakthrough',
    66: 'BlackArmoryRun',
    67: 'Salvage',
    68: 'IronBannerSalvage',
    69: 'PvPCompetitive',
    70: 'PvPQuickplay',
    71: 'ClashQuickplay',
    72: 'ClashCompetitive',
    73: 'ControlQuickplay',
    74: 'ControlCompetitive',
    75: 'GambitPrime',
    76: 'Reckoning',
    77: 'Menagerie'
}


def bungie_response_wrapper(original_func):
    def wrapper_func(*args, **kwargs):
        resp = original_func(*args, **kwargs)
        try:
            resp = resp.json()
        except:
            raise Exception("API Access error")
        if resp.get("ErrorCode") != 1:
            raise Exception(f"ErrorCode: {resp.get('ErrorCode')}, ErrorStatus: {resp.get('ErrorStatus')}, Message: {resp.get('Message')}")
        return resp.get("Response")
    return wrapper_func


# http://destinydevs.github.io/BungieNetPlatform/docs/services/Destiny2/Destiny2-SearchDestinyPlayer
@bungie_response_wrapper
def search_destiny_player(displayName):
    return requests.get(f"https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/-1/{urllib.parse.quote(displayName)}", headers=HEADERS)


# http://destinydevs.github.io/BungieNetPlatform/docs/services/Destiny2/Destiny2-GetProfile
@bungie_response_wrapper
def get_profile(membershipType, membershipId, components: list):
    _components = map(str, components)
    return requests.get(f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{membershipId}/?components={','.join(_components)}", headers=HEADERS)


# http://destinydevs.github.io/BungieNetPlatform/docs/services/Destiny2/Destiny2-GetActivityHistory
@bungie_response_wrapper
def get_activity_history(membershipType, membershipId, characterId, count=3, mode=0, page=0):
    data = {"count": count, "mode": mode, "page": page}
    return requests.get(f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Account/{membershipId}/Character/{characterId}/Stats/Activities/", headers=HEADERS, params=data)


# http://destinydevs.github.io/BungieNetPlatform/docs/services/GroupV2/GroupV2-GetGroupByName
@bungie_response_wrapper
def get_group_by_name(group_name, group_type=1):
    # params = {"groupName": group_name, "groupType": group_type}
    resp = requests.get(f"https://www.bungie.net/Platform/GroupV2/Name/{group_name}/{group_type}", headers=HEADERS)
    return resp


# http://destinydevs.github.io/BungieNetPlatform/docs/services/GroupV2/GroupV2-GetGroup
@bungie_response_wrapper
def get_group(group_id):
    return requests.get(f"https://www.bungie.net/Platform/GroupV2/{group_id}/", headers=HEADERS)


# http://destinydevs.github.io/BungieNetPlatform/docs/services/GroupV2/GroupV2-GetMembersOfGroup
@bungie_response_wrapper
def get_members_of_group(group_id, current_page=1):
    return requests.get(f"https://www.bungie.net/Platform/GroupV2/{group_id}/Members/", headers=HEADERS)


# http://destinydevs.github.io/BungieNetPlatform/docs/services/Destiny2/Destiny2-GetPostGameCarnageReport
@bungie_response_wrapper
def get_post_game_carnage_report(activity_id):
    return requests.get(f"https://www.bungie.net/Platform/Destiny2/Stats/PostGameCarnageReport/{activity_id}", headers=HEADERS)


def get_online_clan_members(clan_name):
    # 그룹명 -> 그룹ID
    group_id = get_group_by_name(clan_name)["detail"]["groupId"]
    # 그룹ID -> 클랜원 명단
    members = get_members_of_group(group_id).get("results")
    return filter(lambda x: x.get("isOnline"), members)


# def print_what_clan_members_doing(clan_name):
#     members = get_online_clan_members(clan_name)
#     for member in members:
#         display_name = member["destinyUserInfo"]["displayName"]
#         membership_id = member.get("destinyUserInfo", {}).get("membershipId")
#         membership_type = member.get("destinyUserInfo", {}).get("membershipType")
#         # 현재 활동 로딩하는 부분
#         profile = get_profile(membership_type, membership_id, [204])
#         if not profile.get("characterActivities", {}).get("data"):
#             print(display_name + " 프로필 비공개 또는 캐릭터 없음")
#             continue
#         # find recent character
#         acc_recent_time = datetime.datetime(1970, 1, 1)
#         for char, data in profile["characterActivities"]["data"].items():
#             recent_time = datetime.datetime.strptime(data["dateActivityStarted"], "%Y-%m-%dT%H:%M:%SZ")
#             if recent_time > acc_recent_time:
#                 acc_recent_time = recent_time
#                 recent_character = char
#         # character_activities
#         data = profile["characterActivities"]["data"][recent_character]
#         print(f"{display_name}\t{DestinyActivityModeType[data.get('currentActivityModeType', -1)]}")
#     return


# http://destinydevs.github.io/BungieNetPlatform/docs/schemas/Destiny-HistoricalStats-DestinyHistoricalStatsPeriodGroup
# def inspect_gambit_actiyity(activity, get_fireteam=False) -> (bool, int):
#     # return 0 if no problem
#     # Return False if private match (maybe)
#     if activity["activityDetails"]["isPrivate"]:
#         return False
#     instance_id = activity["activityDetails"]["instanceId"]
#     stats = {x: y["basic"]["value"] for x, y in activity["values"].items()}
#     if stats["completed"] and stats["kills"] < 2 and stats["score"] == 0:
#         pgcr = get_post_game_carnage_report(instance_id)
#         fireteam = sum(1 for i in pgcr["entries"] if i["values"]["fireteamId"]["basic"]["value"] == stats["fireteamId"])
#     return


# def scan_all_gambit_record(membership_id, membership_type, max_yellow_card=3):
#     profile = get_profile(membership_type, membership_id, components=[100])["profile"]
#     character_ids = profile["data"]["characterIds"]
#     results = []
#     yellow_card = 0
#     for char_id in character_ids:
#         # print(f"현재 캐릭터 ID: {char_id}")
#         page = 0
#         while True:
#             activities = get_activity_history(membership_type, membership_id, char_id, count=100, mode=75, page=page).get("activities", [])
#             for activity in activities:
#                 # 사설경기일경우(?) 건너뛰기
#                 if activity["activityDetails"]["isPrivate"]:
#                     continue
#                 instance_id = activity["activityDetails"]["instanceId"]
#                 stats = {x: y["basic"]["value"] for x, y in activity["values"].items()}
#                 # results.append("처치: {kills}\t티끌 반납: {score}".format(**stats))
#                 if stats["completed"] and stats["kills"] < 2 and stats["score"] == 0:
#                     # 지정한 횟수 이하로 3인이하 잠수, 탈주안함, 처치 2이하, 티끌반납 0개인경우 PCGR 검사
#                     if yellow_card <= max_yellow_card:
#                         pgcr = get_post_game_carnage_report(instance_id)
#                         fireteam = sum(1 for i in pgcr["entries"] if i["values"]["fireteamId"]["basic"]["value"] == stats["fireteamId"])
#                         results.append(f"미활동 감지 : https://destinytracker.com/d2/pgcr/{instance_id} | 활동 내 화력팀원: {fireteam}명")
#                     else:
#                         results.append(f"미활동 감지 : https://destinytracker.com/d2/pgcr/{instance_id}")
#             if len(activities) < 100:
#                 break
#             page += 1
#     return results


def main():
    return


if __name__ == "__main__":
    main()
