# Halo Server Query
Query and retrieve information about Halo: Custom Edition servers (based on [Chaosvex's "Halo-Status"](https://github.com/Chaosvex/Halo-Status))

# example
Example Usage:
``` python
from pprint import PrettyPrinter
from haloserverquery import queryServer

printer = PrettyPrinter(indent=4)

serverInfo = queryServer("127.0.0.1", 2302)
printer.pprint(serverInfo)
```
Example Output:

``` text
{   'dedicated': '1',
    'final': 'Sapp',
    'fraglimit': '50',
    'game_classic': '0',
    'game_flags': '26',
    'gamemode': 'openplaying',
    'gametype': 'Slayer',
    'gamevariant': 'TeamPistols',
    'gamever': '01.00.10.0621',
    'hostname': 'server name',
    'hostport': '23900',
    'mapname': 'carousel',
    'maxplayers': '16',
    'nextmap': 'carousel',
    'nextmode': 'TeamPistols',
    'numplayers': '7',
    'password': '0',
    'player_flags': '1101561860,136',
    'players': {   0: {   'name': 'Extreme',
                          'ping': '108',
                          'score': '0',
                          'slot': 0,
                          'team': '0'},
                   1: {   'name': 'ext',
                          'ping': '90',
                          'score': '30',
                          'slot': 1,
                          'team': '1'},
                   2: {   'name': 'sL Bryan',
                          'ping': '90',
                          'score': '13',
                          'slot': 2,
                          'team': '0'},
                   3: {   'name': 'Lizmari',
                          'ping': '96',
                          'score': '8',
                          'slot': 3,
                          'team': '0'},
                   4: {   'name': 'timefreeze',
                          'ping': '110',
                          'score': '2',
                          'slot': 4,
                          'team': '0'},
                   5: {   'name': 'gjldfaghgk',
                          'ping': '85',
                          'score': '1',
                          'slot': 5,
                          'team': '1'},
                   6: {   'name': 'PAUL S2',
                          'ping': '98',
                          'score': '4',
                          'slot': 6,
                          'team': '1'}},
    'queryid': '1.1',
    'sapp': '10.2.1 CE',
    'sapp_flags': '1',
    'score_t0': '23',
    'score_t1': '37',
    'team_t0': 'Red',
    'team_t1': 'Blue',
    'teamplay': '1'}
```

