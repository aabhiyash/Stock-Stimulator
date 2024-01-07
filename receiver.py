import socket
from threading import Thread
from taipy.gui import Gui, State, invoke_callback, get_state_id
import pandas as pd 

HOST = "127.0.0.1"
PORT = 5050

state_id_list = []

def on_init(state: State):
    state_id = get_state_id(state)
    if (state_id := get_state_id(state)) is not None:
        state_id_list.append(state_id)


def client_handler(gui: Gui, state_id_list: list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, _ = s.accept()
    while True:
        if data := conn.recv(1024):
            print(f"Data received: {data.decode()}")
            if hasattr(gui, "_server") and state_id_list:
                invoke_callback(
                    gui, state_id_list[0], update_received_data, (str(data.decode()),)
                )
        else:
            print("Connection closed")
            break


def update_received_data(state: State, val):
    state.received_data = val
    tempdata = state.data
    tempdata["Price"][0] = tempdata["Price"][1]
    tempdata["Price"][1] = tempdata["Price"][2]
    tempdata["Price"][2] = tempdata["Price"][3]
    tempdata["Price"][3] = state.received_data.split(",")[0]
    state.Company_name = state.received_data.split(",")[1]
    state.data = tempdata


title = "Stock Stimulator By Abhiyash" 
path = "logo.png"
Company_name = "Tata"
Company_minp = "340"
Company_maxp = "740"

def abhiyash(state):
    print("Hey Hello abhiyash")
    print(state)
    print(path)
    print(state.Company_minp)

    with open("data.txt", "w") as f:
        f.write(f"{state.Company_name},{state.Company_minp},{state.Company_maxp}")    


data = {
    "Date": pd.date_range("2023-01-01", periods=4, freq="D"),
    "Price": [222,419.7,662.7,323.5],
    
}


received_data = "No Data"

md = """
<|text-center | 
<|{path}|image|>

<|{title}|hover_text=welcome to stock screener|> 

Name of Stock: <|{Company_name}|input|>

Min Price: <|{Company_maxp}|input|>

Max Price: <|{Company_minp}|input|>

<|Button Label|button|on_action=abhiyash|>

<|{title}|hover_text={Company_name}|>

<|{data}|chart|mode=lines|x=Date|y[1]=Price|line[1]=dash|>


>

"""
gui = Gui(page=md)

t = Thread(
    target=client_handler,
    args=(
        gui,
        state_id_list,
    ),
)
t.start()

gui.run(title="Receiver Page")
