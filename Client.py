"""
Author          - Aidan Zastrow
Description     - Connects the a Server that you will need to define
at the variable host. Then sets up multiple threads to receive and
Send messages on. Also sets up another thread to display the
LCD messages on.
"""

from I2CLCD1602 import PrintLCD
import socket
import threading

ClientMultiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 18

print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

def receive_messages(connection : socket.socket,smt : threading.Thread):
    """
    Receive messages from the server and update the lcd display
    """
    lcd_conn = PrintLCD(smt)
    lcd_conn.start()
    while smt.is_alive():
        data_bytes = connection.recv(2048)
        data = data_bytes.decode('utf-8')
        print(data)
        lcd_conn.update("TODO",data)
    

def send_messages(connection : socket.socket):
    """
    Send messages to the server
    """
    while True:
        Input = input()
        if Input.lower() == 'q' or Input.lower() == "quit":
            break
        else:
            connection.sendall(Input.encode('utf-8'))

send_messages_thread = threading.Thread(target= send_messages, args=(ClientMultiSocket,))
send_messages_thread.start()

receive_messages_thread = threading.Thread(target= receive_messages, args=(ClientMultiSocket,send_messages_thread,))
receive_messages_thread.start()


send_messages_thread.join()
ClientMultiSocket.shutdown(socket.SHUT_RDWR)
receive_messages_thread.join()

ClientMultiSocket.close()
print("done")