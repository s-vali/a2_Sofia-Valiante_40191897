import socket
import sys

def client_program():
    HOST, PORT = socket.gethostname(), 9999 #since both files are running on the same computer

    client_socket = socket.socket() #instantiate
    client_socket.connect((HOST, PORT)) #connect to the server, is tuple

    #print menu
    print("\nPython DB Menu\n")
    print("1. Find customer")
    print("2. Add customer")
    print("3. Delete customer")
    print("4. Update customer age")
    print("5. Update customer address")
    print("6. Update customer phone")
    print("7. Print report")
    print("8. Exit\n")

    message = input("Select: ") #take input from client initially
    while (message.lower().strip() != '8'):
        client_socket.send(message.encode()) #send message to server
        print(client_socket.recv(9000).decode()) #will show in client terminal
        message = input(" >>> ") #again take input from client
    print("\nProgram ended... Good-Bye!")
    client_socket.close() #close the connection
#end of def client_program()

if __name__ == '__main__':
    client_program()
