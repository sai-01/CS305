import pickle
import socket
import struct
import threading
import time
import zlib

import cv2
import pyaudio

from CONSTANTS import *

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

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            sframe = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
            # 将对象序列化(变量从内存中变成可存储或传输的过程)
            data = pickle.dumps(sframe)
            # 压缩流数据
            zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            try:
                self.sock.sendall(struct.pack("Q", len(zdata)) + zdata)
            except:
                break
            for i in range(3):
                self.cap.read()

    def __del__(self):
        self.sock.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass

    def receive_data(self):
        # conn, address = self.sock.accept()
        data = "".encode("utf-8")
        payload_size = struct.calcsize("Q")  # 结果为8
        cv2.namedWindow(str(self.addr), cv2.WINDOW_NORMAL)

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
            cv2.imshow(str(self.addr), frame)
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
        self.p = pyaudio.PyAudio()  # 实例化PyAudio,并于下面设置portaudio参数
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK
                                  )
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
    #
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
                self.sock.sendall(data)
            except:
                pass



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
        self

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

    # def __del__(self):
    #     self.sock.close()
    #     try:
    #         cv2.destroyAllWindows()
    #     except:
    #         pass

    def receive_data(self):
        # conn, address = self.sock.accept()
        while True:
           data = self.sock.recv(81920)
