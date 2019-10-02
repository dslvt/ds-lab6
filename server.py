import time
import os
import sys
import socket
from threading import Thread
import glob

clients = []
special_symbol = b'~~~~~~~~~~'

#this is server code

class ClientListener(Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock

    # clean up
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()

    def run(self):
        data = self.sock.recv(1024)
        file_name, data = data[:data.find(special_symbol)].decode(), data[data.find(special_symbol)+10:]
        if glob.glob(file_name) != []:
            original_name, extension = file_name.split('.')
            files = glob.glob(original_name+'_copy*')
            max_num = 1
            for fl in files:
                name, ext = fl.split('.')
                name = name[len(original_name)+5] 
                max_num = max(max_num, int(name))
            file_name = original_name + '_copy' + str(max_num+1) + '.' + extension
        f = open(file_name, 'wb')
        print(file_name)
        while True:
            # try to read 1024 bytes from user
            # this is blocking call, thread will be paused here
            # print(data)
            if data.find(special_symbol) != -1:
                data = data[:data.find(special_symbol)]
            f.write(data)
            data = self.sock.recv(1024)
            #print(data)
            if not data:
                # if we got no data – client has disconnected
                self._close()
                f.close()
                statinfo = os.stat(file_name)
                print('size: {}'.format(statinfo.st_size))
                # finish the thread
                return


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 8228))
sock.listen()

while True:
        # blocking call, waiting for new client to connect
        con, addr = sock.accept()
        clients.append(con)
        # start new thread to deal with client
        ClientListener(con).start()