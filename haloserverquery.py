#!/usr/bin/env python3
# Based on https://github.com/Chaosvex/Halo-Status

import socket


def queryServer(ip: str, port=2302):
    """Query a specific halo server and return results as an array"""
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
        return assocArry

    UDP_IP: str = ip
    UDP_PORT: int = port
    MESSAGE: bytes = b"\query"

    sock: socket = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.settimeout(3)

    try:
        data: bytes = sock.recv(2048, 0)
        sock.close()
        return parseData(data)
    except socket.timeout as err:
        sock.close()
        return None





def main():
    """Main Function"""

    ip: str = input("Enter IP: ")
    port: int = int(input("Enter Port: "))

    print(
        queryServer(ip, port)
    )


if __name__ == "__main__":
    main()

