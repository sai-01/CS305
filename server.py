from CONSTANTS import *
from server_sockets import *
import socket
import threading

'''
    The main server file implements the concurrency via multi-threading.
    You can only modify the total ports and related server socket initiation here.

    If you want to implement the concurrency with other methods,
    you can create a new file to replace this file.
'''


def socket_listen(port):
    '''
        Start a threading function to listen a port
    '''
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the address
    sock.bind(('', port))
    # Socket listen
    sock.listen(5)
    # Start to listen
    # client_list = []
    # conn, address = sock.accept()
    while True:
        # Wait to client to connect
        conn, address = sock.accept()

        ''' 
            Modify here
        '''
        # client_list.append(conn)
        # Start the server socket threading class
        if port == XXPORT:
            # Initiate the Port1Socket and start
            Port1Socket = ServerSocket(conn, address)
            Port1Socket.start()

            # print(Port1Socket.data)
            # Port1Socket(conn,address).start()
            # for connected in client_list:
            #     connected.sendall(Port1Socket.data)
        elif port == YYPORT:
            # Initiate the Port2Socket and start
            Port2Socket = Audio_ServerSocket(conn, address)
            Port2Socket.start()
            # zdata = Port2Socket.start()
            # for connected in client_list:
            #     connected.sendall(Port2Socket.data)
        elif port == ZZPORT:
            # Initiate the Port1Socket and start
            Port3Socket = msg_ServerSocket(conn, address)
            Port3Socket.start()
        elif port == AAPORT:
            # Initiate the Port1Socket and start
            Port4Socket = desktop_ServerSocket(conn, address)
            Port4Socket.start()


if __name__ == "__main__":
    # Threading lists
    ths = []

    # Ports which need to listen
    '''Modify here'''
    ports = [XXPORT, YYPORT, ZZPORT, AAPORT]

    # Add threadings
    for port in ports:
        ths.append(threading.Thread(target=socket_listen, args=(port,)))
    # Start threading
    try:
        for th in ths:
            th.start()
    except Exception as e:
        print(e)
