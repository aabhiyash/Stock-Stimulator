from taipy import Gui
import pandas as pd 

data = {
    "Date": pd.date_range("2023-01-01", periods=4, freq="D"),
    "Min": [222,419.7,662.7,323.5],
    "Max": [28.6,68.2,666.5,173.5]
}


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

page = """
<|text-center | 
<|{path}|image|>

<|{title}|hover_text=welcome to stock screener|> 

Name of Stock: <|{Company_name}|input|>

Min Price: <|{Company_maxp}|input|>

Max Price: <|{Company_minp}|input|>

<|Run Stimulation|button|on_action=abhiyash|>

<|{title}|hover_text=Your Simulation|>

<|{data}|chart|mode=lines|x=Date|y[1]=Min|y[2]=Max|line[1]=dash|color[2]=blue||>

>

"""
if __name__ == "__main__":
    app = Gui(page)
    app.run(use_reloader=True)