# BIG-DRIFTER
![DRIFTER](DRIFTER.png)
BIG DRIFTER IS WATCHING YOU

## Information
Find Gambit/Gambit Prime AFK user from clan member list.

## How to use
1. `API_KEY`에 번지 API KEY, `TELEGRAM_TOKEN`에 텔레그램 봇 토큰, `DISCORD_WEBHOOK`에 디스코드 웹훅 URL 입력.
2. 주기적으로 `main.py`를 cron 돌리시면 됩니다. 권장 시간은 5분~10분 사이.

## TODO
- [ ] `bungie_api.py` 대신 다른 비동기 지원 모듈 사용 (중요)
- [x] Discord 지원
- [ ] 특정 Telegram 유저에게만 봇 단위로 클랜/유저 감지 메시지 전송
- [ ] 다수의 클랜 동시 감시
- [ ] 여러 종류의 활동(일반 갬빗, 강철 깃발, 경쟁 등) 감시