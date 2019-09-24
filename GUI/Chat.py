from threading import Thread
from tkinter import *

#----------Connection info--------------#
host = '127.0.0.1'
port = 9943
#---------------------------------------#

def conn(active_conn2server, active_client, username):
    #nested function for creating 'closure' - avoids using global variables
    #also, hides functions that are not needed outside conn

    print("Script has passed to the Chat_room class")
    client_socket = active_client
    print(client_socket)

    def receive():
        # Thread for communication from server + insert user in text box
        while True:
            try:
                message = client_socket.recv(1024).decode('utf8')
                message_list.insert(END, '\n' + message)
            except OSError:  # Error handling in case client leaves
                break

    def send(event=None):
        # handling sending message to the server
        message = usermessage.get()  # message from entry
        usermessage.set('')  # clear pre message
        client_socket.send(bytes(message, 'utf8'))

        if message == "QQQ":
            client_socket.close()  # destroys chat window
            window.destroy()  # destroy chat room
            sys.exit(0)  # main gui hidden, kills app off

    def closing_window(event=None):
        usermessage.set("QQQ")
        send()

    window = Toplevel()
    window.geometry("600x450")
    window.title("Chatroom")
    window.configure(background="light blue")

    loggedin_frame = Frame(window)
    loggedin_frame.configure(relief='groove', borderwidth='2', background="white")
    message_frame = Frame(window)
    message_frame.configure(relief='groove', borderwidth='2', background='white')
    text_frame = Frame(window)
    text_frame.configure(relief='groove', borderwidth='2', background='white')

    usermessage = StringVar()
    usermessage.set("Type here.")

    user_list = Text(loggedin_frame, wrap=WORD)
    scroller = Scrollbar(message_frame)
    message_list = Text(message_frame,wrap=WORD, yscrollcommand=scroller.set)
    my_message = Entry(text_frame, textvariable=usermessage)
    my_message.bind("<Return>", send)
    send_button = Button(text_frame, text="Send", command=send)

    #placing
    loggedin_frame.place(relx=0.017, rely=0.022, relheight=0.967, relwidth = 0.125)
    message_frame.place(relx=0.15, rely=0.022, relheight=0.833, relwidth = 0.825)
    text_frame.place(relx=0.15, rely=0.867, relheight=0.122, relwidth = 0.825)
    user_list.place(relx=0.133, rely=0.023, relheight=0.952, relwidth=0.72)
    message_list.place(relx=0.02, rely=0.027, relheight=0.944, relwidth=0.917)
    scroller.place(relx=0.949, rely=0.027, height=351, width=14)
    my_message.place(relx=0.02, rely=0.182, height=30, relwidth=0.776)
    send_button.place(relx=0.808, rely=0.182, height=34, width=77)

    message_list.insert(END, "Welcome: " + username)
    user_list.insert(END, username + '\n')
    receive_thread = Thread(target=receive)  # Starts thread for monitoring servertraffic
    receive_thread.start()
    window.protocol("WM_DELETE_WINDOW", closing_window)