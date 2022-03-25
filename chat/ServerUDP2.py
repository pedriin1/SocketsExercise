import socket
from threading import Thread


config = {
    "name" : "Cliente 2",
    "sendPort" : 22036,
    "recvPort" : 22037,
    "ipServer" : "192.168.15.64",
    "ipSender": "192.168.15.64",
    "message" : ""
}

def runServer():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    sock.bind((config["ipServer"], config["recvPort"])) 
    while True:
        data, _ = sock.recvfrom(1024)
        print("Recebido: ", data.decode('utf-8'))


def runClient():    
    while True:
        MENSAGEM = str(input(">>"))
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.sendto(MENSAGEM.encode('UTF-8'), (config["ipSender"], config["sendPort"]))
        

if __name__ == '__main__':
    Thread(target = runServer).start()
    Thread(target = runClient).start()