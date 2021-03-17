import socket
import threading
import time
import tkinter as tk


HEADER = 1024
PORT =5500
SERVER = 'localhost'
ADDR = (SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED"
clients=[]
client_names=[]
s=[]
######################################################
window = tk.Tk()
window.title("Server")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Connect", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

#########################################################################
def start_server():
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)
    server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(10)
    ACCEPT_THREAD = threading.Thread(target=wait_for_connection,args=(server,))
    ACCEPT_THREAD.start()
    

def wait_for_connection(server):
    while True:
        client, addr = server.accept()
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,addr,)).start()
        
def handle_client(client,addr):
    client_name  = client.recv(4096)
    client.send(bytes("Welcome " + client_name.decode(FORMAT) + ". Use 'exit' to quit","utf8"))
    client_names.append(client_name)
    update_client_names_display(client_names)

    while True:
        msg=client.recv(4096).decode(FORMAT)
        if not msg: break
        if msg == "exit": break

        c_id=get_client_index(clients,client)
        c_name=client_names[c_id]

        for c in clients:
            if c!= client:
                print("yo")
                c.send(bytes(c_name.decode(FORMAT)+": "+msg,"utf-8"))
                print("ho raha")

    c_id= get_client_index(clients, client)
    clients_names.pop(c_id)
    clients.pop(c_id)
    client.send(bytes("BYE!","utf-8"))
    client.close()

    update_client_names_display(clients_names) 
        

def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c,"\n")
    tkDisplay.config(state=tk.DISABLED)

def get_client_index(clients,client):
    c_id=0
    for connection in clients:
        if connection == client:
            break
        c_id+=1
    return c_id

def stop_server():
    pass

window.mainloop()
