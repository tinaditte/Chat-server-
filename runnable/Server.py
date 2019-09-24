import hashlib
import os
import threading
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from GUI import Register

#----------Connection info--------------#
host = "localhost"
port = 9943
#---------------------------------------#

#Creating server socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(10)

#Dicts of clients and addresses
clients = {}
addresses = {}

def accept_connections():
    #Function for taking incomming conn and start credential checking threads
    while True:
        client, client_address = server_socket.accept()
        print("Connection from: " + str(client_address) + ". Passing to credential check...")

        #Thread for credential check w/ client + client add args
        vali_thread = Thread(target=validate_user, args=(client, client_address))
        vali_thread.start()

def validate_user(client, client_address):
    lock = threading.Lock()
    client_validation = client.recv(1024).decode("utf8")
    login_type, user, password, password2 = client_validation.split()

    print("Attempted " + login_type + " with username: " + user + " and password: " + password)

    if login_type == 'try_login':
        if checking(user, password) == True:
            print(user + " is validated. Passing to client handle")
            client.send(bytes("valid", "utf8"))    #confirm validation for user
            addresses[client] = client_address
            chat_thread = Thread(target=client_handler, args=(client, user))  #Starts a new thread, pass it to client_handler
            chat_thread.start()
        else:
            print(user + " wrong password.")
            client.send(bytes("invalid", "utf8"))

    elif login_type == 'try_register':
        with lock: #automatically enters w lock, blocking other transaction, leaves it realeased
            if Register.check_if_user_exists(user):
                client.send(bytes('User exists', 'utf8'))
            elif Register.check_if_match(password, password2) == False:
                print("Error, password mismatch")
                client.send(bytes("mismatch", "utf8"))
            else:
                Register.create_password(user, password)
                client.send(bytes("Register was successfull", "utf8"))
                xhat_thread = Thread(target=client_handler, args=(client, user)) #Starts a new thread, pass it to client_handler
                xhat_thread.start()
    else:
        print("Unexpected login type." + login_type)

def client_handler(client, user):
    #Function for when user reaches chatroom.
    #And to broadcast messages between users

    welcome = "Welcome %s. If you wish to exit, please type QQQ \n." % user
    client.send(bytes(welcome, "utf8"))
    clients[client] = user #user is added to client list
    user_join = '\n%s has joined the chat.' %user
    broadcast(bytes(user_join, "utf8"))

    while True:
        try:
            message = client.recv(1024) #receives messages from users
            if message != bytes("QQQ", "utf8"):
                broadcast(message, user + ": ") #pass message to be broadcasted
            else: #if user leaves the chat
                client.send(bytes("QQQ", "utf8"))
                client.close()
                del clients[client] #delete client from list
                exit_message = "%s has left the chat." %user
                broadcast(bytes(exit_message, "utf8"))
                break
        except ConnectionResetError:
            print(user + " has exited the chat")
            break

def broadcast(user_message, prefix='', ):
    #Function for relaying messages from each user to the rest, via client dict.
    #Every client in client dict receives the message, by iterating through the list
    for client in clients:
        client.send(bytes(prefix, "utf8") + user_message)

def checking(username, password):
    #Comparing entered password, in hashed, salted, digested form
    #with the salted, digested password in user file
    password = hashlib.sha256(password.encode())
    saltystring = Register.get_salty()
    password.update(saltystring.encode())

    if os.path.isfile('../users/' + username):
        #if user exists -> read content as bytes
        with open('../users/' + username, 'rb') as file_handle:
            hashedpass = file_handle.read(32)
            #if hashedpass is read the same as digested password
        if password.digest() == hashedpass:
            return True
        else:
            return False
    else:
        print("Error")

print("Server listening on host: " + host + " on port " +  str(port))
print("Waiting for connections...")
accept_thread = Thread(target=accept_connections)   #accept each thread bf validation
accept_thread.start()
accept_thread.join()    #join acceot_thread --> script waits for completion before going to close