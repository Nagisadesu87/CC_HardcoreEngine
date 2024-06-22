# CC HardcoreEngine

MCDR Plugin for a UHC-like Minecraft Hardcore Surivival Competition System.

## Features

- Competition Time Countdown
- Border Shrink System: time-scheduled border shrinking, border shrinking time countdown/ warning
- Eliminate Player Rank
- Player Position Annouce System: automatically annouce every players' position to each player
- Every Funcitons are Configurable

## Commands

| Command format| Introduction|
|---|---|
|`!!hce help`| Show help message, aka `!!hce`|
|`!!hce start [<time>]`| Start the game now or in setted time|
|`!!hce config set <config_id> [<value>]`| Modify the plugin config|
|`!!hce config query <config_id>`| Query a config's setting|

## Config files
hce/config.json
```json
{
    "permission": { // Command permissions
    "start": 3,
    "config": 3
    },
    "system": { // RCON settings
        "rconPort": ["127.0.0.1"], 
        "rconPassword": "password"
    },
    "game": {
        "roundCount": 6, // in times, the round count of the game
        "roundTime": [1200, 1200, 1200, 1200, 1200, 1200], // in sc, the time for each round
        "borderRadius": [2500, 2000, 1500, 1000, 500, 50], // in block, the radius of border for each round
        "borderTime": [300, 300, 300, 300, 300, 360],  // in sec, the shrinking time of border for each round
        "borderWarningTime": 15,  // in sec, notify players when the time left for border shrink
        "borderFinalCenterRandom": true, // Enable if the center position of the final border is random-decided
        "borderFinalCenterRange": [20, 20] // The position of the center of the final border (if is not set to random)
    }, 
    "info": {
        "bossbar": {
            "showRoundCountdown": true, // Enable the round countdown bar
            "barColor": "yellow" // Color of the countdown bar
        }, 
        "sidebar": {
            "titleText": {"text":"2486生存戰", "color":"aqua", "bold":"true"}, // in raw JSON format, Title text of the sidebar
            "showEliminateRank": true, // Enable showing the eliminate rank of deid player on the sidebar
            "eliminateRankText": "排名", // Prefix text of the eliminate rank
            "showNextBorderRadius": true, // Enable showing the border radius of next round on the sidebar
            "nextBorderRadiusText": "下次邊界半徑" // Prefix text of the next round border radius
        }, 
        "actionbar": {
            "playerBorderDistanceMode": "permanent", // Mode of the border distance notification to players
            "playerBorderDistanceTime": 300 // in sec, show the notification when the time left if mode is set to "time"
        },
        "chat" : {
            "playerPosMode": "roundEnd", // Mode of the player position annouce funcution
            "playerPosTime": 1200 // in sec, the time cycle to annouce players' position if the mode is set to "time"
        }
    }
}
```