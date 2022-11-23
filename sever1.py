import socket
from collections import OrderedDict

def printMenu(connection):
    connection.send("\n\nPython DB Menu\n".encode())
    connection.send("1. Find customer\n".encode())
    connection.send("2. Add customer\n".encode())
    connection.send("3. Delete customer\n".encode())
    connection.send("4. Update customer age\n".encode())
    connection.send("5. Update customer address\n".encode())
    connection.send("6. Update customer phone\n".encode())
    connection.send("7. Print report\n".encode())
    connection.send("8. Exit\n\n".encode())
    connection.send("Select: ".encode())

if __name__ == '__main__':

    #get host name
    HOST = socket.gethostname()
    PORT = 9999

    server_socket = socket.socket() #instantiate socket object
    server_socket.bind((HOST, PORT)) #takes tuple as argument, binds host address and port together
    
    #configure how many clients the server can listen to simultaneously
    server_socket.listen(2)

    #load database from text file, only once
    database = open('data.txt', 'r+')
    sorted_dict = {}
    while True:
        line = database.readlines()
        #end of file is reached
        if not line:
            break 
        #deliminate the read line into cells of array
        for cell in line:
            info_array = cell.split("|")
            name = info_array[0]
            name  = " " + name #in case file read has an empty name that does not contain spaces 
            if(name.isspace()):
                continue
            sorted_dict.update({info_array[0]: tuple(info_array)}) #dictionary: key(string), value(tuple)

    #alphebetize keys of dictionary
    sorted_dict = OrderedDict(sorted(sorted_dict.items()))
             
    #maintain constant server connection unless killed in terminal
    while True:
        connection, address = server_socket.accept() #accept new connection

        #while recieving input from client, perform switch cases
        while True:
            data = connection.recv(1024).decode() #recieve data (stream) from client, will not recieve data greater than 1024 bytes
            if not data:
                break #if data is not received break

            #switch case for DB Menu
            if(str(data) == "1"):
                connection.send("(1. Find customer) Customer Name: ".encode()) #send data to the client
                key = connection.recv(1024).decode()
                if str(key) in sorted_dict: #if the key can be found in the dictionary
                    connection.send("Server response: ".encode())
                    message = ""
                    for info in sorted_dict[key]: #obtain info of the key in the dictionary
                        message = info.strip() + "|"
                        connection.send(message.encode())
                else:
                    message = "Server response: " + str(key) + " not found in database" #key could not be found in dictionary
                    connection.send(message.encode())
                printMenu(connection) #set the option for the menu back
            elif(str(data) == "2"):
                connection.send("(2. Add customer) Customer Name: ".encode()) #prompt user
                name = connection.recv(1024).decode() #recieve input
                #if the customer already exists
                if str(name) in sorted_dict:
                    connection.send("Server response: Customer already exists. ".encode())
                else:
                    connection.send("(2. Add customer) Customer Age: ".encode())
                    age = connection.recv(1024).decode()
                    connection.send("(2. Add customer) Customer Address: ".encode())
                    address = connection.recv(1024).decode()
                    connection.send("(2. Add customer) Customer Phone: ".encode())
                    phone = connection.recv(1024).decode()
                    sorted_dict.update({name: (name, age, address, phone)}) #update dictionary with new customer
                    connection.send("Server response: Customer has been added. ".encode())
                printMenu(connection) #set the option for the menu back
            elif(str(data) == "3"):
                connection.send("(3. Delete customer) Customer Name: ".encode())
                rcv = connection.recv(1024).decode()
                if str(rcv) in sorted_dict:
                    sorted_dict.pop(str(rcv)) #pop the key from the dictionary
                    message = "Server response: " + str(rcv) + " has been removed."
                    connection.send(message.encode())
                else:
                    message = "Server response: " + str(rcv) + " not found in database"
                    connection.send(message.encode())
                printMenu(connection)
            elif(str(data) == "4"):
                connection.send("(4. Update customer age) Customer Name: ".encode())
                key = connection.recv(1024).decode()
                if str(key) in sorted_dict:
                    connection.send("(4. Update customer age) Update Age: ".encode())
                    update = connection.recv(1024).decode()
                    tuple_to_list = list(sorted_dict[key]) #convert tuple to list to change its elements
                    tuple_to_list[1] = update #age occurs in the 2 cell of the tuple
                    sorted_dict[key] = tuple(tuple_to_list) #convert list back to tuple and store as value for the respective key in the dictionary
                    message = "Server response: " + str(key) + " has been updated."
                    connection.send(message.encode())
                else:
                    message = "Server response: " + str(key) + " not found in database"
                    connection.send(message.encode())
                printMenu(connection)
            elif(str(data) == "5"):
                connection.send("(5. Update customer address) Customer Name: ".encode())
                key = connection.recv(1024).decode()
                if str(key) in sorted_dict:
                    connection.send("(5. Update customer address) Update Address: ".encode())
                    update = connection.recv(1024).decode()
                    tuple_to_list = list(sorted_dict[key])
                    tuple_to_list[2] = update
                    sorted_dict[key] = tuple(tuple_to_list)
                    message = "Server response: " + str(key) + " has been updated."
                    connection.send(message.encode())
                else:
                    message = "Server response: " + str(key) + " not found in database"
                    connection.send(message.encode())
                printMenu(connection)
            elif(str(data) == "6"):
                connection.send("(6. Update customer phone) Customer Name: ".encode())
                key = connection.recv(1024).decode()
                if str(key) in sorted_dict:
                    connection.send("6. Update customer phone) Update Phone: ".encode())
                    update = connection.recv(1024).decode()
                    tuple_to_list = list(sorted_dict[key])
                    tuple_to_list[3] = update
                    sorted_dict[key] = tuple(tuple_to_list)
                    message = "Server response: " + str(key) + " has been updated."
                    connection.send(message.encode())
                else:
                    message = "Server response: " + str(key) + " not found in database"
                    connection.send(message.encode())
                printMenu(connection)
            elif(str(data) == "7"):
                connection.send("\n** Python DB Contents **\n".encode())
                #alphebetize keys of dictionary
                sorted_dict = OrderedDict(sorted(sorted_dict.items()))
                message = ""
                for i in sorted_dict.values():    
                    for j in i:
                        message += j.strip() + "|"
                    message += "\n"
                connection.sendall(message.encode())
                printMenu(connection)
            else:
                connection.send("\nInvalaid selection. Try again! \n ".encode())
                printMenu(connection)

