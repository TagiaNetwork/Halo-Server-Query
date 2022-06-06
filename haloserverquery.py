#!/usr/bin/env python3
# Based on https://github.com/Chaosvex/Halo-Status

import socket

def decodePlayerFlags(player_flags: str):
    """Decode player flags"""
    player_flags = int(player_flags)
    return {
        'NumberOfLives': player_flags & 3,
        'MaximumHealth': (player_flags >> 2) & 7,
        'Shields': (player_flags >> 5) & 1,
        'RespawnTime': (player_flags >> 6) & 3,
        'RespawnGrowth': (player_flags >> 8) & 3,
        'OddManOut': (player_flags >> 10) & 1,
        'InvisiblePlayers': (player_flags >> 11) & 1,
        'SuicidePenalty': (player_flags >> 12) & 3,
        'InfiniteGrenades': (player_flags >> 14) & 1,
        'WeaponSet': (player_flags >> 15) & 15,
        'StartingEquipment': (player_flags >> 19) & 1,
        'Indicator': (player_flags >> 20) & 3,
        'OtherPlayersOnRadar': (player_flags >> 22) & 3,
        'FriendIndicators': (player_flags >> 24) & 1,
        'FriendlyFire': (player_flags >> 25) & 3,
        'FriendlyFirePenalty': (player_flags >> 27) & 3,
        'AutoTeamBalance': (player_flags >> 29) & 1
    }

def decodeVehicleFlags(vehicle_flags: str):
    """Decode vehicle flags"""
    vehicle_flags = int(vehicle_flags)
    return {
        'Vehicle respawn': (vehicle_flags & 7),
        'Red vehicle set': (vehicle_flags >> 3) & 15,
        'Blue vehicle set': (vehicle_flags >> 7) & 15
    }

def decodeGameFlags(game_flags: str):
    """Decode player flags"""
    game_flags = int(game_flags)
    decoded_flags = {'Game type': game_flags & 7}
    if decoded_flags['Game type'] == 1: # CTF
        decoded_flags['Assault'] = (game_flags >> 3) & 1
        decoded_flags['Flag must reset'] = (game_flags >> 5) & 1
        decoded_flags['Flag at home to score'] = (game_flags >> 6) & 1
        decoded_flags['Single flag'] = (game_flags >> 7) & 7
    elif decoded_flags['Game type'] == 2: # Slayer
        decoded_flags['Death bonus'] = (game_flags >> 3) & 1
        decoded_flags['Kill penalty'] = (game_flags >> 5) & 1
        decoded_flags['Kill in order'] = (game_flags >> 6) & 1
    elif decoded_flags['Game type'] == 3: # Oddball
        decoded_flags['Random start'] = (game_flags >> 3) & 1
        decoded_flags['Speed with ball'] = (game_flags >> 5) & 3
        decoded_flags['Trait with ball'] = (game_flags >> 7) & 3
        decoded_flags['Trait without ball'] = (game_flags >> 9) & 3
        decoded_flags['Ball type'] = (game_flags >> 11) & 3
        decoded_flags['Ball spawn count'] = (game_flags >> 13) & 31
    elif decoded_flags['Game type'] == 4: # KOTH
        decoded_flags['Moving hill'] = (game_flags >> 3) & 1
    elif decoded_flags['Game type'] == 5: # Race
        decoded_flags['Race type'] = (game_flags >> 3) & 3
        decoded_flags['Team scoring'] = (game_flags >> 5) & 3
    return decoded_flags

def parseData(data: bytes):
    """Parse server query response data"""
    queryArray = data.decode("utf-8").split("\\")
    queryArray.pop(0)

    numPlayers = int(queryArray[19])

    tempArray = queryArray.copy()
    if 'player_0' in queryArray:
        playerOffset = queryArray.index('player_0')
        scoreOffset = playerOffset + (numPlayers * 2);
        pingOffset = playerOffset + (numPlayers * 4);
        teamOffset = playerOffset + (numPlayers * 6);

        del tempArray[playerOffset : playerOffset + numPlayers*8]

    assocArry = dict()
    i = 0
    while i < len(tempArray):
        assocArry[tempArray[i]] = tempArray[i+1]
        i += 2


    assocArry["players"] = dict()
    if "player_0" in queryArray:
        i = 0
        pCount = 1
        while i < numPlayers:
            assocArry['players'][i] = dict()
            assocArry['players'][i]['slot'] = i
            assocArry['players'][i]['name'] = queryArray[playerOffset + pCount]
            assocArry['players'][i]['score'] = queryArray[scoreOffset + pCount]
            assocArry['players'][i]['ping'] = queryArray[pingOffset + pCount]
            assocArry['players'][i]['team'] = queryArray[teamOffset + pCount]
            pCount += 2
            i += 1
    
    flags = assocArry['player_flags'].split(',') + [assocArry['game_flags']]
    assocArry['player_flags'] = decodePlayerFlags(flags[0])
    assocArry['vehicle_flags'] = decodeVehicleFlags(flags[1])
    assocArry['game_flags'] = decodeGameFlags(flags[2])
    
    return assocArry

def queryServer(ip: str, port=2302):
    """Query a specific halo server and return results as an array"""

    UDP_IP: str = ip
    UDP_PORT: int = port
    MESSAGE: bytes = b"\\query"

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
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
    print(
        queryServer(ip, port)
    )


if __name__ == "__main__":
    main()

