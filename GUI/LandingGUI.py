from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter import messagebox

from GUI import Register as Register, Chat

#----------Connection info--------------#

host = '127.0.0.1'
port = 9943
#---------------------------------------#

def GUI(master):     #always runs when class is called
    """
    Landing page, accepts master as argument
    Class initialize regestration_screen and chat_room locally,
    so function from the classes can be reached by reference.
    Launching registration_screem by calling locally declared launch_registering_screen

    () for calling toplevel function, it doesn't run on reference only
    chat_room class has toplevel() located in _init_ and will run by instance

    """
    def on_register(event=None):
        Register.register_gui()
        master.withdraw()

    def closing():
        master.destroy()
        sys.exit(0)

    #Gui settings
    master.title("Landing Page")
    master.geometry("600x450+765+446")
    master.configure(background="light blue")

    user = StringVar
    passw = StringVar

    #Welcome frame+label, and choice frame+label:
    welcome_frame = Frame(master)
    welcome_frame.place(relx=0.033, rely=0.044, relheight=0.189, relwidth =0.942)
    welcome_frame.configure(relief='groove')
    welcome_frame.configure(borderwidth="2")
    welcome_frame.configure(relief="groove")
    welcome_frame.configure(background="white")
    label_wel = Label(welcome_frame)
    label_wel.place(relx=0.071, rely=0.235, height=51, width=494)
    label_wel.configure(background="white")
    label_wel.configure(font=("Arial", 40))
    label_wel.configure(text='Welcome!')

    label_choice_frame = Frame(master)
    label_choice_frame.place(relx=0.3, rely=0.267, relheight=0.144, relwidth=0.675)
    label_choice_frame.configure(relief='groove')
    label_choice_frame.configure(borderwidth="2")
    label_choice_frame.configure(relief="groove")
    label_choice_frame.configure(background="white")
    label_choice = Label(label_choice_frame)
    label_choice.place(relx=0.049, rely=0.154, height=41, width=364)
    label_choice.configure(background="white")
    label_choice.configure(font=("Arial", 14))
    label_choice.configure(text='What would you like to do?')

    left_canvas = Canvas(master)
    left_canvas.place(relx=0.033, rely=0.267, relheight=0.651, relwidth = 0.238)
    left_canvas.configure(background="white")
    left_canvas.configure(borderwidth="2")
    left_canvas.configure(insertbackground="black")
    left_canvas.configure(relief="ridge")
    left_canvas.configure(selectforeground="black")

    #login frame
    login_frame = Frame(master)
    login_frame.place(relx=0.3, rely=0.444, relheight=0.478, relwidth = 0.675)
    login_frame.configure(relief='groove')
    login_frame.configure(borderwidth="2")
    login_frame.configure(relief="groove")
    login_frame.configure(background="white")
    #Login username and password configs
    label_name = Label(login_frame)
    label_name.place(relx=0.074, rely=0.186, height=41, width=104)
    label_name.configure(background="white")
    label_name.configure(font=("Arial", 12))
    label_name.configure(text='Username')
    label_password = Label(login_frame)
    label_password.place(relx=0.074, rely=0.419, height=41, width=104)
    label_password.configure(background="white")
    label_password.configure(font=("Arial", 12))
    label_password.configure(text='Password')
    label_or = Label(login_frame)
    label_or.place(relx=0.321, rely=0.744, height=21, width=17)
    label_or.configure(background="white")
    label_or.configure(text='or')
    #entry configs
    entry_name = Entry(login_frame, textvariable=user)
    entry_name.place(relx=0.395, rely=0.233, height=20, relwidth=0.405)
    entry_name.configure(background="white")
    entry_password = Entry(login_frame, textvariable=passw, show='*')
    entry_password.place(relx=0.395, rely=0.465, height=20, relwidth=0.405)
    entry_password.configure(background="white")
    #button config
    button_log = Button(login_frame, text="Login", command=lambda: loggingin(entry_name.get(), entry_password.get()))
    button_log.place(relx=0.123, rely=0.698, height=34, width=67)
    button_reg = Button(login_frame, text="Register", command=on_register)
    button_reg.place(relx=0.395, rely=0.698, height=34, width=67)

    master.protocol("WM_DELETE_WINDOW", closing)

def loggingin(username, password, master):
    """
    When 'login' button is pressed
    Sends username and password to server, along with login type
    Server sends back answer whether the login was valid og invalid
    Client_socket is placed here to initiate new connection each time a password validation is requested.
    Otherwise, the original connection dies and program will have issues to re-establish
    """
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connection has been started by login attempt.")
    print("Client Socket info: " + str(client_socket))
    validation_data = 'try_login' + ' ' + username + ' ' + password + ' ' + password
    client_socket.send(bytes(validation_data, "utf8"))

    server_message = client_socket.recv(1024).decode("utf8")

    if server_message == "valid":
        print("User validation confirmed. Open chat room...")
        master.withdraw()
        #Starts chat room session
        Thread(target=Chat.conn, args=(server_message, client_socket, username)).start()

    elif server_message == "invalid":
        messagebox.showinfo("Invalid password and/or username.")
        client_socket.close()

    else:
        print(server_message)
        client_socket.close()