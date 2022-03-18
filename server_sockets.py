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
meeting_list = []


class Meeting():
    def __init__(self):
        self.meetingID = random.randint(100000, 999999)
        self.conn = None
        self.clients_addrs = []
        self.clients_conns_m = []
        self.clients_conns_v = []
        self.clients_conns_a = []
        self.clients_conns_d = []
        self.control_addr = None
        self.control_conn = None
        self.host = None

    def add_client_conn_m(self, client_conn):
        self.clients_conns_m.append(client_conn)

    def add_client_conn_v(self, client_conn):
        self.clients_conns_v.append(client_conn)

    def add_client_conn_a(self, client_conn):
        self.clients_conns_a.append(client_conn)

    def add_client_conn_d(self, client_conn):
        self.clients_conns_d.append(client_conn)

    def add_client_addr(self, client_addr):
        self.clients_addrs.append(client_addr)

    def remove_client(self, client_addr):
        self.clients_addrs.remove(client_addr)


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
        global meeting_list
        flag_once = 1
        payload_size = struct.calcsize("Q")  # 结果为8

        while True:
            self.data = b''
            while len(self.data) < payload_size:
                self.data += self.conn.recv(81920)
            packed_size = self.data[:payload_size]
            self.data = self.data[payload_size:]
            msg_size = struct.unpack("Q", packed_size)[0]
            while len(self.data) < msg_size:
                self.data += self.conn.recv(81920)
            zframe_data = self.data[:msg_size]
            self.data = zframe_data
            for meeting in meeting_list:
                for i in range(len(meeting.clients_addrs)):
                    if meeting.clients_addrs[i][0] == self.addr[0]:
                        if flag_once == 1:
                            meeting.add_client_conn_v(self.conn)
                            flag_once = 0
                        for j in range(len(meeting.clients_conns_v)):
                            if meeting.clients_conns_v[j] != self.conn:
                                meeting.clients_conns_v[j].sendall(
                                    struct.pack("Q", len(self.addr[0].encode())) + self.addr[0]
                                    .encode() + struct.pack("Q", len(self.data)) +
                                    self.data)
                        break
                    else:
                        continue
                else:
                    print('6')
                    continue
                break


class Audio_ServerSocket(threading.Thread):
    def __init__(self, conn, addr):
        super(Audio_ServerSocket, self).__init__()
        # The connection to send data
        self.conn = conn
        # The address of the client
        self.addr = addr
        self.data = "".encode("utf-8")

    def run(self):
        global meeting_list
        flag_once = 1
        while True:
            try:
                data = self.conn.recv(81920)
                for meeting in meeting_list:
                    for i in range(len(meeting.clients_addrs)):
                        if meeting.clients_addrs[i][0] == self.addr[0]:
                            if flag_once == 1:
                                meeting.add_client_conn_a(self.conn)
                                flag_once = 0
                            for j in range(len(meeting.clients_conns_a)):
                                if meeting.clients_conns_a[j] != self.conn:
                                    meeting.clients_conns_a[j].sendall(data)
                            break
                    else:
                        continue
                    break
            except:
                pass


class msg_ServerSocket(threading.Thread):
    def __init__(self, conn, addr):
        super(msg_ServerSocket, self).__init__()
        self.conn = conn
        self.addr = addr
        self.data = "".encode("utf-8")

    def run(self):
        global meeting_list
        while 1:
            try:
                data = self.conn.recv(1024)
                data = data.decode()
                if data == '1':
                    m = Meeting()
                    meeting_list.append(m)
                    m.host = self.addr[0]
                    self.conn.sendall(str(m.meetingID).encode())
                elif data == '2':
                    for meeting in meeting_list:
                        for i in range(len(meeting.clients_addrs)):
                            if meeting.clients_addrs[i][0] == self.addr[0]:
                                meeting.remove_client(client_addr=self.addr)
                                try:
                                    meeting.clients_conns_a.remove(meeting.clients_conns_a[i])
                                    meeting.clients_conns_v.remove(meeting.clients_conns_v[i])
                                    meeting.clients_conns_d.remove(meeting.clients_conns_d[i])
                                except:
                                    pass
                                self.conn.sendall('88'.encode())
                                break
                        else:
                            continue
                        break
                elif data == '3':
                    for meeting in meeting_list:
                        for i in range(len(meeting.clients_addrs)):
                            if meeting.clients_addrs[i][0] == self.addr[0]:
                                s = ''
                                for addr in meeting.clients_addrs:
                                    s1, s2 = addr
                                    s += s1 + ','
                                self.conn.sendall(s.encode())
                                print(s)
                                break
                        else:
                            continue
                        break
                elif 'ip' in data:
                    ip = data[2:]
                    for meeting in meeting_list:
                        for i in range(len(meeting.clients_addrs)):
                            if meeting.clients_addrs[i][0] == self.addr[0]:
                                for j in range(len(meeting.clients_addrs)):
                                    if ip == meeting.clients_addrs[j][0]:
                                        meeting.control_addr = self.addr
                                        meeting.control_conn = self.conn
                                        meeting.clients_conns_m[j].sendall('if'.encode())
                                        break
                        else:
                            continue
                        break
                elif data == 'y':
                    for meeting in meeting_list:
                        for i in range(len(meeting.clients_addrs)):
                            if meeting.clients_addrs[i][0] == self.addr[0]:
                                meeting.control_conn.sendall('y'.encode())
                                break
                        else:
                            continue
                        break
                elif data == 'n':
                    for meeting in meeting_list:
                        for i in range(len(meeting.clients_addrs)):
                            if meeting.clients_addrs[i][0] == self.addr[0]:
                                meeting.control_conn.sendall('n'.encode())
                                break
                        else:
                            continue
                        break
                elif 'close' in data:
                    mid = data[5:]
                    for meeting in meeting_list:
                        if meeting.meetingID == int(mid):
                            if meeting.host == self.addr[0]:
                                self.conn.sendall('Close Success'.encode())
                                meeting_list.remove(meeting)
                                break
                            else:
                                self.conn.sendall('No Way'.encode())
                                break
                else:
                    flag = 0
                    for meeting in meeting_list:
                        if meeting.meetingID == int(data):
                            meeting.add_client_addr(self.addr)
                            meeting.add_client_conn_m(self.conn)
                            self.conn.sendall('ok'.encode())
                            flag = 1
                            break
                    if flag == 0:
                        self.conn.sendall('no'.encode())

            except:
                pass


class desktop_ServerSocket(threading.Thread):
    def __init__(self, conn, addr):
        super(desktop_ServerSocket, self).__init__()
        self.conn = conn
        self.addr = addr
        self.data = "".encode("utf-8")

    def run(self):
        global meeting_list
        flag_once = 1
        while True:
            try:
                data = self.conn.recv(1024)
                if data is not None:
                    for meeting in meeting_list:
                        for i in range(len(meeting.clients_addrs)):
                            if meeting.clients_addrs[i][0] == self.addr[0]:
                                if flag_once == 1:
                                    meeting.add_client_conn_d(self.conn)
                                    flag_once = 0
                                for j in range(len(meeting.clients_conns_d)):
                                    if meeting.clients_conns_d[j] != self.conn:
                                      meeting.clients_conns_d[j].sendall(data)
                                break
                        else:
                            continue
                        break
            except:
                pass
