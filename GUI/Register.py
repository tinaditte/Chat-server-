import hashlib
import os
import random
import string
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter import messagebox
from GUI import Chat

#----------Connection info--------------#
host = '127.0.0.1'
port = 9943
#---------------------------------------#

def submit_user(username, password, password2):
    # Connection initiated when register is chosen
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))
    print(client_socket)
    validation_data = 'try_register' + ' ' + username + ' ' + password + ' ' + password2
    client_socket.send(bytes(validation_data, 'utf8'))

    # receive server repsonse
    server_message = client_socket.recv(1024).decode('utf8')

    if server_message == 'Register was successfull':
        print("Registered and validated. Off to chat room...")
        register_screen.destroy()
        print("User has registered, passing active client to chatroom class")
        #Thread is initiated and started to handle chat session
        Thread(target=Chat.conn, args=(server_message, client_socket, username)).start()
    elif server_message == 'User exists':
        messagebox.showinfo("Username is taken!")
        client_socket.close() #kills current conn
    elif server_message == 'mismatch':
        messagebox.showinfo("The passwords doesn't match.")
        client_socket.close()
    else:
        print('Unexpected return message from server' + server_message)
        client_socket.close()

def register_gui():
    global register_screen
    register_screen = Toplevel()
    register_screen.title("Register")
    register_screen.geometry('300x400')
    register_screen.configure(borderwidth="2", background="light blue")

    reg_frame = Frame(register_screen)
    reg_frame.place(relx=0.067, rely=0.05, relheight=0.913, relwidth = 0.883)
    reg_frame.configure(relief='groove', borderwidth="2", background="white")

    label_question = Label(reg_frame, text="Fill out form: ")
    label_question.place(relx=0.075, rely=0.055, height=41, width=224)
    label_question.configure(background="white", font=("Arial", 10))

    global username_reg
    global password_reg
    username_reg = StringVar
    password_reg = StringVar

    label_regname = Label(reg_frame, text="Username", background="white")
    entry_regname = Entry(reg_frame, textvariable=username_reg)
    label_regpass = Label(reg_frame, text="Password", background="white")
    entry_regpass = Entry(reg_frame, textvariable=password_reg, show='*')
    label_regpass2 = Label(reg_frame, text="Repeat password", background="white")
    entry_regpass2 = Entry(reg_frame, textvariable=password_reg, show='*')
    button_submit = Button(reg_frame, text="Submit", command=lambda: submit_user(entry_regname.get(),
                                                                                      entry_regpass.get(), entry_regpass2.get()))

    label_gen = Label(reg_frame, text="Password generator", background="white")
    button_gen = Button(reg_frame, text="Generate", command=generator_GUI)

    #placing
    label_regname.place(relx=0.038, rely=0.219, height=21, width=79)
    entry_regname.place(relx=0.528, rely=0.219, height=20, relwidth = 0.392)
    label_regpass.place(relx=0.038, rely=0.329, height=21, width=79)
    entry_regpass.place(relx=0.528, rely=0.329, height=20, relwidth=0.392)
    label_regpass2.place(relx=0.038, rely=0.411, height=41, width=109)
    entry_regpass2.place(relx=0.528, rely=0.438, height=20, relwidth=0.392)
    button_submit.place(relx=0.075, rely=0.548, height=24, width=67)
    label_gen.place(relx=0.038, rely=0.685, height=41, width=126)
    button_gen.place(relx=0.075, rely=0.795, height=24, width=68)

    register_screen.protocol("WM_DELETE_WINDOW", closing)

def closing():
    register_screen.destroy()
    sys.exit(0)

def check_if_user_exists(username):
    if os.path.isfile('../users/' + username):
        return True
    else:
        return False

def get_salty():
    #Get the size of the salty file
    saltylength = os.path.getsize("../secret/salty")
    with open("../secret/salty", 'r', encoding="utf-8") as file_handle:
        #Reads length of salty(saltylength), saves it in a variable: saltystring
        saltystring = file_handle.read(saltylength)
        return saltystring

def create_password(username, password):
    # password hashed to 64 chars
    # fixed size 256bit (32 bytes)
    password = hashlib.sha256(password.encode())
    saltystring = get_salty()
    #feeder password bytes with saltystring in bytes.
    password.update(saltystring.encode())

    with open("../users/" + username, 'wb') as file_handle:
        #adder password bytes, digested (sammenlagt) in file user
        file_handle.write(password.digest())
        #digest: 16 bytes string, incl non ascii chars.

def check_if_match(password, password2):
    if password == password2:
        return True
    else:
        return False

def check_if_registered(username):
    if os.path.isfile('../users/' + username):
        return True
    else:
        return False

#-----------------------------------------------------#
"""
Generation part of the program
"""
#-----------------------------------------------------#

def generator_GUI():
    password_list = []
    global pg_screen
    global gen_copy
    global gen_entry
    pg_screen = Toplevel()
    pg_screen.title("Generating password")
    pg_screen.geometry('250x200')
    pg_screen.configure(background="light blue")

    pg_frame = Frame(pg_screen)
    pg_frame.configure(relief="groove", borderwidth="2", background="white")

    gen_label = Label(pg_frame, text="Gemerate a password")
    gen_entry = Entry(pg_frame, widt=200)
    gen_button = Button(pg_frame, text="Generate", command=generator)
    gen_copy = Button(pg_frame, text="Use",)

    #placing
    pg_frame.place(relx=0.08, rely=0.1, relheight=0.825, relwidth=0.86)
    gen_label.place(relx=0.093, rely=0.182, height=21, width=164)
    gen_entry.place(relx=0.093, rely=0.424, height=30, relwidth=0.809)
    gen_button.place(relx=0.093, rely=0.727, height=24, width=58)
    gen_copy.place(relx=0.558, rely=0.727, height=24, width=39)

def generator():
    number = string.digits
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    symbol = string.punctuation
    password = ''.join(random.choice(number + lowercase + uppercase + symbol) for x in range(15))
    print(password)
    str_password = str(password)
    gen_entry.delete(0, END)
    gen_entry.insert(0, str_password)