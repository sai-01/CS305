import pickle
import random
import socket
import struct
import threading
import time
import zlib

import cv2
import numpy as np
import pyaudio
from PIL import ImageGrab
from cv2 import cvtColor, COLOR_RGB2BGR

from CONSTANTS import *
import ctrl

'''
    We provide a base class here.
    You can create new sub classes based on it.
'''


class ClientSocket():
    '''
        The main process of the ClientSocket is:
        Receive: receive data -> analyze the data -> take actions (send data or others)
        Send: construct data -> send data -> (optional) wait for reply (i.e., receive data)
    '''

    def __init__(self, addr, client, sport=None):
        '''
            @Parameters
                addr: server address
                client: the registed client
                sport: the binded port of this socket
        '''
        # Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.release()
        # You can bind the certain port with the client
        if sport is not None:
            self.sock.bind(('', sport))
        # else:
        #     self.sock.bind(('', XXPORT))
        # # The registered client
        # self.sock.listen(2)
        self.client = client
        # Protocol related - Header
        # If they are with the same format, you can use
        # self.header_format = None
        # self.header_size = 0
        # Instead
        self.rheader_format = None  # The receiving header format
        self.rheader_size = 0  # The size of the receiving header
        self.sheader_format = None  # The sending header format
        self.sheader_size = 0  # The size of the sending header

        # If you want to connect to the server right now
        while True:
            try:
                self.sock.connect(self.addr)
                print("Connected")
                break
            except:
                print("Could not connect to the server" + str(self.addr))
        # Create a receive_server_data threading
        self.send_thread = threading.Thread(target=self.send_data)
        self.receive_thread = threading.Thread(target=self.receive_data)

        # If you want to start to receive data right now
        # self.receive_thread.start()

    def send_data(self):
        '''
            Receive the data from the sever
            It should be a threading function
        '''
        while True:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                sframe = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
                # ??????????????????(???????????????????????????????????????????????????)
                data = pickle.dumps(sframe)
                # ???????????????
                zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
                try:
                    self.sock.sendall(struct.pack("Q", len(zdata)) + zdata)
                except:
                    break
                for i in range(3):
                    self.cap.read()

    def close_cap(self):
        self.cap.release()

    def open_cap(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        self.sock.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass

    def receive_data(self):
        data = "".encode("utf-8")
        payload_size = struct.calcsize("Q")  # ?????????8

        while True:
            while len(data) < payload_size:
                data += self.sock.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            addr_size = struct.unpack("Q", packed_size)[0]
            while len(data) < addr_size:
                data += self.sock.recv(81920)

            frameName = data[:addr_size].decode()
            data = data[addr_size:]
            cv2.namedWindow(frameName, cv2.WINDOW_NORMAL)

            while len(data) < payload_size:
                data += self.sock.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_size)[0]
            while len(data) < msg_size:
                data += self.sock.recv(81920)

            zframe_data = data[:msg_size]
            data = data[msg_size:]
            frame_data = zlib.decompress(zframe_data)
            frame = pickle.loads(frame_data)
            cv2.imshow(frameName, frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break


class AudioClientSocket():
    '''
        The main process of the ClientSocket is:
        Receive: receive data -> analyze the data -> take actions (send data or others)
        Send: construct data -> send data -> (optional) wait for reply (i.e., receive data)
    '''

    def __init__(self, addr, client, sport=None):
        '''
            @Parameters
                addr: server address
                client: the registed client
                sport: the binded port of this socket
        '''
        # Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        self.p = pyaudio.PyAudio()  # ?????????PyAudio,??????????????????portaudio??????
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK
                                  )
        self.send_flag = False
        # self.stream.close()
        self.stream1 = self.p.open(format=FORMAT,
                                   channels=CHANNELS,
                                   rate=RATE,
                                   output=True,
                                   frames_per_buffer=CHUNK
                                   )
        # You can bind the certain port with the client
        if sport is not None:
            self.sock.bind(('', sport))
        # # The registered client
        # self.sock.listen(2)
        self.client = client
        # Protocol related - Header
        # If they are with the same format, you can use
        # self.header_format = None
        # self.header_size = 0
        # Instead
        self.rheader_format = None  # The receiving header format
        self.rheader_size = 0  # The size of the receiving header
        self.sheader_format = None  # The sending header format
        self.sheader_size = 0  # The size of the sending header

        # If you want to connect to the server right now
        while True:
            try:
                self.sock.connect(self.addr)
                print("Connected")
                break
            except:
                print("Could not connect to the server" + str(self.addr))
        # Create a receive_server_data threading
        # self.send_thread = threading.Thread(target=self.send_data)
        # self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread = threading.Thread(target=self.receive_server_data)
        self.send_thread = threading.Thread(target=self.send_data_to_server)
        # If you want to start to receive data right now
        # self.receive_thread.start()

    #
    def __del__(self):
        self.sock.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        if self.stream1 is not None:
            self.stream1.stop_stream()
            self.stream1.close()
        self.p.terminate()

    def receive_server_data(self):
        while True:
            try:
                data = self.sock.recv(81920)
                self.stream1.write(data)
            except:
                pass

    def send_data_to_server(self):
        while True:
            try:
                data = self.stream.read(81920)
                if self.send_flag:
                    self.sock.sendall(data)
                else:
                    data = None

            except:
                pass

    def close_stream(self):
        self.send_flag = False
        # self.stream.close()

    def open_stream(self):
        self.send_flag = True


class msg_ClientSocket():
    '''
        The main process of the ClientSocket is:
        Receive: receive data -> analyze the data -> take actions (send data or others)
        Send: construct data -> send data -> (optional) wait for reply (i.e., receive data)
    '''

    def __init__(self, addr, client, sport=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        if sport is not None:
            self.sock.bind(('', sport))
        self.client = client
        self.accept = None

        while True:
            try:
                self.sock.connect(self.addr)
                print("Connected")
                break
            except:
                print("Could not connect to the server" + str(self.addr))
        # Create a receive_server_data threading
        # self.send_thread = threading.Thread(target=self.send_data)
        # self.receive_thread = threading.Thread(target=self.receive_data)
        # If you want to start to receive data right now
        # self.receive_thread.start()

    def send_msg(self, data):
        '''
            Receive the data from the sever
            It should be a threading function
        '''
        self.sock.sendall(data.encode())

    def receive_data(self):
        # conn, address = self.sock.accept()
        while True:
            data = self.sock.recv(81920)
            if data is not None:
                if data.decode('utf-8') == 'ok':
                    print("Welcome!")
                    return 1
                elif data.decode('utf-8') == 'no':
                    print("Wrong MeetingID!")
                    return 0
                elif data.decode('utf-8') == '88':
                    print("Bye~")
                    return 0
                elif data.decode('utf-8') == 'if':
                    # accept = self.accept
                    # print("accept:", self.accept)
                    accept = input("Accept or not?(y/n)")
                    return accept
                elif data.decode('utf-8') == 'n':
                    return 'No'
                elif data.decode('utf-8') == 'y':
                    return 'Yes'
                else:
                    print(data.decode('utf-8'))
                    return data.decode('utf-8')

    def send_accept(self, accept):
        self.accept = accept
        # print("self.a:" + self.accept)



class desktop_ClientSocket():
    '''
        The main process of the ClientSocket is:
        Receive: receive data -> analyze the data -> take actions (send data or others)
        Send: construct data -> send data -> (optional) wait for reply (i.e., receive data)
    '''

    def __init__(self, addr, client, sport=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        if sport is not None:
            self.sock.bind(('', sport))
        self.client = client
        self.buf_size = 1024
        self.agree = False
        self.receive = False

        while True:
            try:
                self.sock.connect(self.addr)
                print("Connected")
                break
            except:
                print("Could not connect to the server" + str(self.addr))
        # Create a receive_server_data threading
        self.send_thread = threading.Thread(target=self.send_data)
        self.receive_thread = threading.Thread(target=self.receive_data)
        # If you want to start to receive data right now
        # self.receive_thread.start()

    def send_data(self):
        '''
            Receive the data from the sever
            It should be a threading function
        '''
        while True:
            while self.agree:
                frame = np.asarray(ImageGrab.grab())
                sframe = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
                # ??????????????????(???????????????????????????????????????????????????)
                data = pickle.dumps(sframe)
                # ???????????????
                zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
                try:
                    self.sock.sendall(struct.pack("Q", len(zdata)) + zdata)
                except:
                    break

    def receive_data(self):
        data = "".encode("utf-8")
        payload_size = struct.calcsize("Q")  # ?????????8

        while True:
            while len(data) < payload_size:
                data += self.sock.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_size)[0]
            while len(data) < msg_size:
                data += self.sock.recv(81920)

            zframe_data = data[:msg_size]
            data = data[msg_size:]
            frame_data = zlib.decompress(zframe_data)
            frame = pickle.loads(frame_data)
            frame = cvtColor(frame, COLOR_RGB2BGR)
            # print(frame)
            cv2.imshow('share_screen', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
