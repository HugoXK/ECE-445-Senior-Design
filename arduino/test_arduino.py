# from pyfirmata import Arduino, util
# import pyfirmata
# import time 
# board = Arduino('/dev/ttyACM0')
# it = util.Iterator(board)
# it.start()
# pin_trig = board.get_pin('d:12:o')
# pin_echo = board.get_pin('d:11:i')

# while(1):
#     pin_trig.write(0)
#     time.sleep(0.002)
#     pin_trig.write(1)
#     time.sleep(0.01)
#     print(value)


import serial
import socket
import time
from threading import Thread
ser = serial.Serial("/dev/ttyACM0",9600,timeout=0.5)

val_distance = -1
val_all = None

def set_motor(value = 1):
    ser.write(str(value).encode("iso-8859-15"))
    # time.sleep(1)
    # ch = ser.read(10)
    # print(ch)
    # ch = ch.decode("iso-8859-15")
    # print(ch)

def read_force():
    ch = ser.readline()
    val = ch.decode("iso-8859-15")
    force = int(val)
    return force

def show_line():
    while(1):
        ch = ser.readline()
        val = ch.decode("iso-8859-15")
        print(val)

def show_all():
    global val_all
    while(True):
        ch = ser.readline()
        val = ch.decode("iso-8859-15")
        # end = time.time()
        if(val):
            try:
                # print (val.strip("\n"))
                val_all = val.strip("\n")
                # num = int(val.split('.')[0].strip("\n"))
                # val_distance = num
            except:
                continue

def show_distance():
    global val_distance
    while(True):
        ch = ser.readline()
        val = ch.decode("iso-8859-15")
        # end = time.time()
        if(val):
            try:
                num = int(val.split('.')[0].strip("\n"))
                val_distance = num
                # val_distance = num*17/1000
                # print(num*17/1000)
                # if(end - start >=0.5):
                #     return num
            except:
                continue


def write_motor():
    serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 6666
    serversocket.bind((host, port))
    serversocket.listen(5)
    print("[Arduino SERVER] Start")
    while(1):
        clientsocket, addr = serversocket.accept()
        print("[Arduino SERVER] connect %s" % str(addr))
        msg = clientsocket.recv(1024).decode('utf-8')
        clientsocket.close()
        set_motor(int(msg))


def read_all():  
    global val_all

    serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 7777
    serversocket.bind((host, port))
    serversocket.listen(5)
    print("[Arduino SERVER] Start")

    while(1):
        clientsocket, addr = serversocket.accept()
        print("[Arduino SERVER] connect %s" % str(addr))
        msg = str(val_all)
        clientsocket.sendall(msg.encode('utf-8'))
        clientsocket.close()

def read_distance():  
    global val_distance

    serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 7777
    serversocket.bind((host, port))
    serversocket.listen(5)
    print("[Arduino SERVER] Start")

    while(1):
        clientsocket, addr = serversocket.accept()
        print("[Arduino SERVER] connect %s" % str(addr))
        msg = str(val_distance)
        clientsocket.sendall(msg.encode('utf-8'))
        clientsocket.close()

    # while(1):
    #     ch = ser.readline()
    #     val = ch.decode("iso-8859-15")
    #     if(val):
    #         try:
    #             num = int(val.split('.')[0].strip("\n"))
    #             print(num*17/1000)
    #             msg = str(num)
    #             clientsocket, addr = serversocket.accept()
    #             print("[Arduino SERVER] connect %s" % str(addr))
    #             clientsocket.sendall(msg.encode('utf-8'))
    #             clientsocket.close()
    #         except:
    #             continue

if __name__ == "__main__":
    Thread(target=show_all).start()
    # Thread(target=show_distance).start()
    Thread(target=write_motor).start()
    time.sleep(1)
    read_all()
    # read_distance()

    # Thread(target=show_line).start()
    # time.sleep(1)
    # write_motor()
