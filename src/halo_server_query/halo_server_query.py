#!/usr/bin/env python3
# Based on https://github.com/Chaosvex/Halo-Status

import socket

FLAG_STRINGS = {
    # Player Flags
    "NumberOfLives": ["Infinite", 1, 3, 5],
    "MaximumHealth": ["50%", "100%", "150%", "200%", "300%", "400%"],
    "Shields": [1, 0],
    "RespawnTime": [0, 5, 10, 15],
    "RespawnGrowth": [0, 5, 10, 15],
    "OddManOut": [0, 1],
    "InvisiblePlayers": [0, 1],
    "SuicidePenalty": [0, 5, 10, 15],
    "InfiniteGrenades": [0, 1],
    "WeaponSet": [
        "Normal",
        "Pistols",
        "Assault Rifles",
        "Plasma",
        "Sniper",
        "No Sniping",
        "Rocket Launchers",
        "Shotguns",
        "Short Range",
        "Human",
        "Covenant",
        "Classic",
        "Heavy Weapons",
    ],
    "StartingEquipment": ["Custom", "Generic"],
    "Indicator": ["Motion Tracker", "Nav Points", "None"],
    "OtherPlayersOnRadar": ["No", "All", "", "Friends"],
    "FriendIndicators": [0, 1],
    "FriendlyFire": ["Off", "On", "Shields Only", "Explosives Only"],
    "FriendlyFirePenalty": [0, 5, 10, 15],
    "AutoTeamBalance": [0, 1],
    # Vehicle Flags
    "Vehicle respawn": [0, 30, 60, 90, 120, 180, 300],
    "Red vehicle set": [
        "Default",
        "No vehicles",
        "Warthogs",
        "Ghosts",
        "Scorpions",
        "Rocket Warthogs",
        "Banshees",
        "Shades",
        "Custom",
    ],
    "Blue vehicle set": [
        "Default",
        "No vehicles",
        "Warthogs",
        "Ghosts",
        "Scorpions",
        "Rocket Warthogs",
        "Banshees",
        "Shades",
        "Custom",
    ],
    # Game Falgs
    "Game type": [
        "",
        "Capture the Flag",
        "Slayer",
        "Oddball",
        "King of the Hill",
        "Race",
    ],
    # CTF
    "Assault": [0, 1],
    "Flag must reset": [0, 1],
    "Flag at home to score": [0, 1],
    "Single flag": [0, 60, 120, 180, 300, 600],
    # Slayer
    "Death bonus": [1, 0],
    "Kill penalty": [1, 0],
    "Kill in order": [0, 1],
    # Oddball
    "Random start": [0, 1],
    "Speed with ball": ["Slow", "Normal", "Fast"],
    "Trait with ball": ["None", "Invisible", "Extra Damage", "Damage Resistant"],
    "Trait without ball": ["None", "Invisible", "Extra Damage", "Damage Resistant"],
    "Ball type": ["Normal", "Reverse Tag", "Juggernaut"],
    "Ball spawn count": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    # KOTH
    "Moving hill": [0, 1],
    # Race
    "Race type": ["Normal", "Any Order", "Rally"],
    "Team scoring": ["Minimum", "Maximum", "Sum"],
}


def decodePlayerFlags(player_flags):
    """Decode player flags"""
    player_flags = int(player_flags)
    return {
        "NumberOfLives": FLAG_STRINGS["NumberOfLives"][player_flags & 3],
        "MaximumHealth": FLAG_STRINGS["MaximumHealth"][(player_flags >> 2) & 7],
        "Shields": FLAG_STRINGS["Shields"][(player_flags >> 5) & 1],
        "RespawnTime": FLAG_STRINGS["RespawnTime"][(player_flags >> 6) & 3],
        "RespawnGrowth": FLAG_STRINGS["RespawnGrowth"][(player_flags >> 8) & 3],
        "OddManOut": FLAG_STRINGS["OddManOut"][(player_flags >> 10) & 1],
        "InvisiblePlayers": FLAG_STRINGS["InvisiblePlayers"][(player_flags >> 11) & 1],
        "SuicidePenalty": FLAG_STRINGS["SuicidePenalty"][(player_flags >> 12) & 3],
        "InfiniteGrenades": FLAG_STRINGS["InfiniteGrenades"][(player_flags >> 14) & 1],
        "WeaponSet": FLAG_STRINGS["WeaponSet"][(player_flags >> 15) & 15],
        "StartingEquipment": FLAG_STRINGS["StartingEquipment"][
            (player_flags >> 19) & 1
        ],
        "Indicator": FLAG_STRINGS["Indicator"][(player_flags >> 20) & 3],
        "OtherPlayersOnRadar": FLAG_STRINGS["OtherPlayersOnRadar"][
            (player_flags >> 22) & 3
        ],
        "FriendIndicators": FLAG_STRINGS["FriendIndicators"][(player_flags >> 24) & 1],
        "FriendlyFire": FLAG_STRINGS["FriendlyFire"][(player_flags >> 25) & 3],
        "FriendlyFirePenalty": FLAG_STRINGS["FriendlyFirePenalty"][
            (player_flags >> 27) & 3
        ],
        "AutoTeamBalance": FLAG_STRINGS["AutoTeamBalance"][(player_flags >> 29) & 1],
    }


def decodeVehicleFlags(vehicle_flags):
    """Decode vehicle flags"""
    vehicle_flags = int(vehicle_flags)
    return {
        "Vehicle respawn": FLAG_STRINGS["Vehicle respawn"][(vehicle_flags & 7)],
        "Red vehicle set": FLAG_STRINGS["Red vehicle set"][(vehicle_flags >> 3) & 15],
        "Blue vehicle set": FLAG_STRINGS["Blue vehicle set"][(vehicle_flags >> 7) & 15],
    }


def decodeGameFlags(game_flags):
    """Decode player flags"""
    game_flags = int(game_flags)
    decoded_flags = {"Game type": FLAG_STRINGS["Game type"][game_flags & 7]}

    if decoded_flags["Game type"] == "Capture the Flag":
        decoded_flags["Assault"] = FLAG_STRINGS["Assault"][(game_flags >> 3) & 1]
        decoded_flags["Flag must reset"] = FLAG_STRINGS["Flag must reset"][
            (game_flags >> 5) & 1
        ]
        decoded_flags["Flag at home to score"] = FLAG_STRINGS["Flag at home to score"][
            (game_flags >> 6) & 1
        ]
        decoded_flags["Single flag"] = FLAG_STRINGS["Single flag"][
            (game_flags >> 7) & 7
        ]
    elif decoded_flags["Game type"] == "Slayer":
        decoded_flags["Death bonus"] = FLAG_STRINGS["Death bonus"][
            (game_flags >> 3) & 1
        ]
        decoded_flags["Kill penalty"] = FLAG_STRINGS["Kill penalty"][
            (game_flags >> 5) & 1
        ]
        decoded_flags["Kill in order"] = FLAG_STRINGS["Kill in order"][
            (game_flags >> 6) & 1
        ]
    elif decoded_flags["Game type"] == "Oddball":
        decoded_flags["Random start"] = FLAG_STRINGS["Random start"][
            (game_flags >> 3) & 1
        ]
        decoded_flags["Speed with ball"] = FLAG_STRINGS["Speed with ball"][
            (game_flags >> 5) & 3
        ]
        decoded_flags["Trait with ball"] = FLAG_STRINGS["Trait with ball"][
            (game_flags >> 7) & 3
        ]
        decoded_flags["Trait without ball"] = FLAG_STRINGS["Trait without ball"][
            (game_flags >> 9) & 3
        ]
        decoded_flags["Ball type"] = FLAG_STRINGS["Ball type"][(game_flags >> 11) & 3]
        decoded_flags["Ball spawn count"] = FLAG_STRINGS["Ball spawn count"][
            (game_flags >> 13) & 31
        ]
    elif decoded_flags["Game type"] == "King of the Hill":
        decoded_flags["Moving hill"] = FLAG_STRINGS["Moving hill"][
            (game_flags >> 3) & 1
        ]
    elif decoded_flags["Game type"] == "Race":
        decoded_flags["Race type"] = FLAG_STRINGS["Race type"][(game_flags >> 3) & 3]
        decoded_flags["Team scoring"] = FLAG_STRINGS["Team scoring"][
            (game_flags >> 5) & 3
        ]

    return decoded_flags


def parseData(data: bytes):
    """Parse server query response data"""
    queryArray = data.decode("utf-8").split("\\")
    queryArray.pop(0)

    numPlayers = int(queryArray[19])

    tempArray = queryArray.copy()
    if "player_0" in queryArray:
        playerOffset = queryArray.index("player_0")
        scoreOffset = playerOffset + (numPlayers * 2)
        pingOffset = playerOffset + (numPlayers * 4)
        teamOffset = playerOffset + (numPlayers * 6)

        del tempArray[playerOffset : playerOffset + numPlayers * 8]

    assocArry = dict()
    i = 0
    while i < len(tempArray):
        assocArry[tempArray[i]] = tempArray[i + 1]
        i += 2

    assocArry["players"] = dict()
    if "player_0" in queryArray:
        i = 0
        pCount = 1
        while i < numPlayers:
            assocArry["players"][i] = dict()
            assocArry["players"][i]["slot"] = i
            assocArry["players"][i]["name"] = queryArray[
                playerOffset + pCount  # pyright: ignore
            ]
            assocArry["players"][i]["score"] = queryArray[
                scoreOffset + pCount  # pyright: ignore
            ]
            assocArry["players"][i]["ping"] = queryArray[
                pingOffset + pCount  # pyright: ignore
            ]
            assocArry["players"][i]["team"] = queryArray[
                teamOffset + pCount  # pyright: ignore
            ]
            pCount += 2
            i += 1

    flags = assocArry["player_flags"].split(",") + [assocArry["game_flags"]]
    assocArry["player_flags"] = decodePlayerFlags(flags[0])
    assocArry["vehicle_flags"] = decodeVehicleFlags(flags[1])
    assocArry["game_flags"] = decodeGameFlags(flags[2])

    return assocArry


def queryServer(ip: str, port=2302):
    """Query a specific halo server and return results as an array"""

    UDP_IP: str = ip
    UDP_PORT: int = port
    MESSAGE: bytes = b"\\query"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.settimeout(3)

    try:
        data: bytes = sock.recv(2048, 0)
        sock.close()
        return parseData(data)
    except socket.timeout:
        sock.close()
        return None


def main():
    """Main Function"""

    # ip: str = input("Enter IP: ")
    # port: int = int(input("Enter Port: "))

    ip: str = "216.128.147.196"
    port: int = 2302
    print(queryServer(ip, port))


if __name__ == "__main__":
    main()
