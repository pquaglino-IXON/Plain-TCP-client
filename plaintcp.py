# Campionamento a trigger - i dati devono essere inviati entro pochi millisecondi dopo il trigger

import socket
import datetime
import time
import select

host ='192.168.140.1'
port = 9230
localhost = '192.168.140.99'
password = 'abcd'

def log(str):
    with (open('plain tcp log.txt','a')) as f:
        f.write(str + '\n')
        f.close()

def send(str):
    s.send(str.encode())
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logstring = f'{now} {str.replace("\n","\\n")}'
    print(logstring)
    log(logstring)

    ready = select.select([s], [], [], 0.1)
    if ready[0]:
        data = ''
        data = s.recv(1024).decode()
        print(data)
        log(data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
data = ''
data = s.recv(1024).decode()
print (data)

send(f'DEVC {localhost} {password}\n')

c = ''
while c != 'q':
    c = ''
    c = input('> ')
    match c:
        case 'q': 
            s.close()
            quit()
        case 'a':
            send('@a=10\n@b=20\n@c=30\n')
        case 'A':
            send('@a=10\n@b=20\n@c=30\n@trigger=f\n')
        case 'b':
            send('@a=100\n@b=200\n@c=300\n')
        case 'B':
            send('@a=100\n@b=200\n@c=300\n@trigger=f\n')
        case '0':
            send('@trigger=f\n')
        case '1':
            send('@trigger=t\n')
        case 'c':
            send('@trigger=t\n')
            time.sleep(0.1)
            send('@trigger=f\n')
            time.sleep(0.1)
            send('@a=10\n@b=20\n@c=30\n')
        case 'd':
            send('@trigger=t\n')
            time.sleep(0.1)
            send('@trigger=f\n')
            time.sleep(0.1)
            send('@a=100\n@b=200\n@c=300\n')
            