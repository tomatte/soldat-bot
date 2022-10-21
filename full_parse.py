import socket
import re
from struct import unpack

def refreshParse(sock):

    print('parsing')

    players = {}
    info = {}
    
    for i in range(0, 32):
        players[i] = {}
        nameLength = unpack('B', sock.recv(1))[0]
        players[i]['name'] = sock.recv(nameLength)
        sock.recv(24 - nameLength)

    for i in range(0, 32):
        players[i]['team'] = unpack('B', sock.recv(1))[0]

    for i in range(0, 32):
        players[i]['kills'] = unpack('H', sock.recv(2))[0]

    for i in range(0, 32):
        players[i]['deaths'] = unpack('H', sock.recv(2))[0]

    for i in range(0, 32):
        players[i]['ping'] = unpack('B', sock.recv(1))[0]

    for i in range(0, 32):
        players[i]['id'] = unpack('B', sock.recv(1))[0]

    for i in range(0, 32):
        players[i]['ip'] = '.'.join([str(v) for v in unpack('BBBB', sock.recv(4))])

    info['score'] = {
        'alpha': unpack('H', sock.recv(2))[0],
        'bravo': unpack('H', sock.recv(2))[0],
        'charlie': unpack('H', sock.recv(2))[0],
        'delta': unpack('H', sock.recv(2))[0],
    }

    mapLength = unpack('B', sock.recv(1))[0]
    info['map'] = sock.recv(mapLength)
    sock.recv(16 - mapLength)

    info['timeLimit'] = unpack('i', sock.recv(4))[0]
    info['currentTime'] = unpack('i', sock.recv(4))[0]
    info['killLimit'] = unpack('H', sock.recv(2))[0]
    info['mode'] = unpack('B', sock.recv(1))[0]

    print('players: %s') % [v for k, v in players.iteritems() if v['name'] != '']
    print('info: %s') % info

    info['players'] = players
    return info

pw = 'admin\n'
ip = '192.168.18.4'
port = 23073

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

buf = ''
info = {}
while True:
    try:
        data = s.recv(1)
    except Exception as e:
        break

    if not data:
        break

    buf = buf + str(data)

    if re.search('\r?\n$', buf):
        if buf == 'Soldat Admin Connection Established.\r\n':
            print('connected')
            s.send('%s\n' % pw)
        elif buf == 'Welcome, you are in command of the server now.\r\n':
            print('authed')
            s.send('REFRESH\n')
        elif buf == 'REFRESH\r\n':
            print('refresh packet inbound')
            info = refreshParse(s)
        else:
            print(buf)

        buf = ''

print(info)

s.close()