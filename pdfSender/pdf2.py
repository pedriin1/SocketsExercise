
import socket
from threading import Thread
import base64
import math

config = {
    "name" : "Cliente 1",
    "sendPort" : 32036,
    "recvPort" : 32037,
    "ipServer" : "192.168.15.64",
    "ipSender": "192.168.15.64",
}
INTERVAL = 10000
def runServer():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    sock.bind((config["ipServer"], config["recvPort"])) 
    while True:
        data, _ = sock.recvfrom(2**24)
        if b"E980E67BC2F06641F23E62A14329C883C6E31203DF3CF26A4C364DF2E5D9D081" in base64.b64decode(data):
            pdf = b""
            while True:
                data2, _ = sock.recvfrom(2**24)
                if b"469B7098E2FC06049071E9F08AD5C0067F91E8097354892017DDC58E7F9B35CB" in base64.b64decode(data2 + b'=='):
                    break
                pdf += data2
                
            
            file = open('pdfgerado.pdf', 'wb')
            file.write(base64.b64decode(pdf))
            file.close()
            print("PDF recebido")


def runClient():    
    while True:
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        arquivo = input("Digite o caminho do arquivo: ")

        with open(arquivo, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        
        sock.sendto(base64.b64encode(bytes("E980E67BC2F06641F23E62A14329C883C6E31203DF3CF26A4C364DF2E5D9D081", encoding="UTF-8")), (config["ipSender"], config["sendPort"]))


        for i in range(math.floor(len(encoded_string)/INTERVAL)):
            sock.sendto(encoded_string[i*INTERVAL:(i+1) * INTERVAL], (config["ipSender"], config["sendPort"]))
            if i == math.floor(len(encoded_string)/INTERVAL)-1:
                sock.sendto(encoded_string[(i+1)*INTERVAL:len(encoded_string)%INTERVAL + (i+1)*INTERVAL], (config["ipSender"], config["sendPort"]))
                
        sock.sendto(base64.b64encode(bytes("469B7098E2FC06049071E9F08AD5C0067F91E8097354892017DDC58E7F9B35CB", encoding="UTF-8")), (config["ipSender"], config["sendPort"]))
        
        print(len(encoded_string))
        print("PDF enviado")
        

if __name__ == '__main__':
    Thread(target = runServer).start()
    Thread(target = runClient).start()