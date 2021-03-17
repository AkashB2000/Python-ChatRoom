import socket
import threading
import time
import tkinter as tk
from tkinter import messagebox

##########################################################################
window = tk.Tk()
window.title("Client")
username = " "


topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Name:").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)
btnConnect = tk.Button(topFrame, text="Connect", command=lambda : connect())
btnConnect.pack(side=tk.LEFT)
#btnConnect.bind('<Button-1>', connect)
topFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="*********************************************************************").pack()
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="blue")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)


bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)
#################################################################################################



HEADER = 1024
PORT = 5500
SERVER = 'localhost'
ADDR = (SERVER,PORT)
FORMAT='utf8'
DISCONNECT_MESSAGE = "DISCONNECTED"


def connect_to_server(name):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        client.send(bytes(name,"utf8"))
        
        entName.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)
        
        rcv=threading.Thread(target=receive_msg, args=(client,))
        print("yo")
        rcv.start()
    except Exception as e:
        print(e)
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: ")

def connect():
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        username = entName.get()
        connect_to_server(username)
s_list=[]
def temp(client):
    s_list.append(client)
    
def receive_msg(client):
    temp(client)
    while True:
        data=client.recv(1024).decode(FORMAT)
        print("1")
        if not data: break
        print("2")
        texts = tkDisplay.get("1.0", tk.END).strip()
        tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            tkDisplay.insert(tk.END, data)
            print("3")
        else:
            tkDisplay.insert(tk.END, "\n\n"+ data)
            print("4")

        tkDisplay.config(state=tk.DISABLED)
        tkDisplay.see(tk.END)
        print("5")

    client.close()
    window.destroy()

        
def getChatMessage(msg):
    
    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()
    tkDisplay.config(state=tk.NORMAL)
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message") # no line
    else:
        tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")

    tkDisplay.config(state=tk.DISABLED)

    send_message_to_server(msg)

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)

    
    
def send_message_to_server(msg):
    print(s_list[0])
    s_list[0].send(bytes(msg,"utf8"))
    if msg == "exit":
        s_list[0].close()
        window.destroy()
    print("Sending message")


window.mainloop()


    
