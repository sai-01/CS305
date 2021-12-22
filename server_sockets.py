import pickle
import struct
import random

import cv2

from CONSTANTS import *
import threading

'''
    We provide an exmaple ServerSocket here.
    It is a subclass of threading.Thread, that is,
    it is a threading class.
    You can implement different server sockets with 
    different data analyze methods. Or you use this
    example ServerSocket as the only sockect then
    you need to deal with different type of messages
    in one class.

    We also provide a Meeting class which is used to
    record the meeting information.
    We do not provide any information about the Meeting class,
    so you can design it as you like.
'''


class Meeting():
    def __init__(self):
        self.meetingID = random.randint(100000, 999999)
        self.conn = None
        self.clients_addrs = []
        self.clients_conns = []

    def add_client(self, client_conn, client_addr):
        self.clients_addrs.append(client_addr)
        self.clients_conns.append(client_conn)

    def remove_client(self, client_conn, client_addr):
        self.clients_conns.remove(client_conn)
        self.clients_addrs.remove(client_addr)


    # def __del__(self):
    #     for client in self.clients:
    #         client.video_sockets.__del__()
    #         client.audio_sockets.__del__()
global meeting_list

class ServerSocket(threading.Thread):
    def __init__(self, conn, addr):
        super(ServerSocket, self).__init__()
        # The connection to send data
        self.conn = conn
        # The address of the client
        self.addr = addr
        # Protocol related - Header
        # If they are with the same format, you can use
        # self.header_format = None
        # self.header_size = 0
        # Inste
        self.rheader_format = None  # The receiving header format
        self.rheader_size = 0  # The size of the receiving header
        self.sheader_format = None  # The sending header format
        self.sheader_size = 0  # The size of the sending header
        self.data = "".encode("utf-8")

    def run(self):
        # data = "".encode("utf-8")
        payload_size = struct.calcsize("Q")  # 结果为8
        # cv2.namedWindow(str(self.addr), cv2.WINDOW_NORMAL)
        while True:
            while len(self.data) < payload_size:
                self.data += self.conn.recv(81920)
            packed_size = self.data[:payload_size]
            self.data = self.data[payload_size:]
            msg_size = struct.unpack("Q", packed_size)[0]
            while len(self.data) < msg_size:
                self.data += self.conn.recv(81920)

            zframe_data = self.data[:msg_size]

            self.data = zframe_data
            self.conn.sendall(struct.pack("Q", len(self.data)) + self.data)
            # print(self.data)
            # data = self.data[msg_size:]
            # frame_data = zlib.decompress(zframe_data)
            # frame = pickle.loads(frame_data)
            # self.data = pickle.dumps(frame)
            # try:
            #     return struct.pack("Q", len(senddata)) + senddata
            # except:
            #     break
            # cv2.imshow(str(self.addr), frame)
            # if cv2.waitKey(1) & 0xFF == 27:
            #     break


class Audio_ServerSocket(threading.Thread):
    def __init__(self, conn, addr):
        super(Audio_ServerSocket, self).__init__()
        # The connection to send data
        self.conn = conn
        # The address of the client
        self.addr = addr
        self.data = "".encode("utf-8")

    def run(self):
        payload_size = struct.calcsize("Q")  # 返回对应于格式字符串fmt的结构，L为4

        # while True:
        #     while len(self.data) < payload_size:
        #         self.data += self.conn.recv(81920)
        #     packed_size = self.data[:payload_size]
        #     self.data = self.data[payload_size:]
        #     msg_size = struct.unpack("Q", packed_size)[0]
        #     while len(self.data) < msg_size:
        #         self.data += self.conn.recv(81920)
        #     frame_data = self.data[:msg_size]
        #     # data = self.data[msg_size:]
        #     # frames = pickle.loads(frame_data)
        #     # senddata = pickle.dumps(frame_data)
        #     self.conn.sendall(struct.pack("Q", len (frame_data)) + frame_data)

        while 1:
            try:
                data = self.conn.recv(81920)
                self.conn.sendall(data)
            except:
                pass

            # for frame in frames:
            #     self.stream.write(frame, CHUNK)


class msg_ServerSocket(threading.Thread):
    def __init__(self, conn, addr):
        super(msg_ServerSocket, self).__init__()
        self.conn = conn
        self.addr = addr
        self.data = "".encode("utf-8")

    def run(self):
        while 1:
            try:
                data = self.conn.recv(1024)
                data = data.decode()
                if data is not None:
                    m=Meeting()
                    meeting_list.append(m)
                    self.conn.sendall(str(m.meetingID).encode())
            except:
                pass
