import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import csv
import os
from pathlib import Path

#GLOBAL
data = {}
placement_points = {
              "1": 16,
              "2": 12,
              "3": 10,
              "4": 8,
              "5": 8,
              "6": 5,
              "7": 5,
              "8": 5,
              "9": 3,
              "10": 3,
              "11": 3,
              "12": 3,
              "13": 1,
              "14": 1,
              "15": 1,
              "16": 1,
              "17": 0,
              "18": 0
              }

kill_points = 4

COLOR = "#333" #or "white"
TEXT_COLOR = "white" if COLOR == "#333" else "black"


def addfile(root):
    global data
    if not (file := fd.askopenfilename()):
        return None
    
    clear(root)

    with open(file, mode="r", encoding="utf-8-sig") as c:
        reader = csv.DictReader(c)
        check = True if data else False
        for row in reader:
            row = {k.strip():v.strip() for k,v in row.items()}
            points = int(row.get("kill")) * kill_points + placement_points.get(row.get("rank"))

            frame = tk.Frame(root)
            frame.configure(background=COLOR, borderwidth=2)
            
            if check:
                nickname = row.get("nickname")
                data[nickname]["points"] += points
                data[nickname]["row"].append(row)
            else:
                data[row.get("nickname")] = {
                                            "points": points,
                                            "row": [row],
                                            }
    data = {k:v for k,v in sorted(data.items(), key=lambda item:item[1].get("points"), reverse=True)}
    counter, counter2 = 0, 0
    frame.grid()
    for k, v in data.items():
        if counter >= 9:
            counter, counter2 = 0, 1
        
        insideFrame = tk.Frame(frame)
        insideFrame.configure(background=COLOR, highlightbackground=TEXT_COLOR, highlightthickness=1)
        insideFrame.grid(sticky="w", row=counter, column=counter2, padx=50)
        column = 0
        for img in v.get("row"):
           open_img(insideFrame, img).grid(row=0, column=column, columnspan=1, sticky="w")
           column += 1
        open_text(insideFrame, k, v.get("points")).grid(columnspan=len(v.get("row")))

        counter +=1
    

def open_img(frame, row):
    #creating Image
    static = os.path.join(Path(__file__).parent, "static")
    path_to_img = os.path.join(static, row.get('character') + ".png")
    img = Image.open(path_to_img)
    img = img.resize((30, 30), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    lbl_img = tk.Label(frame, image=img)
    lbl_img.image = img
    lbl_img.configure(background=COLOR)

    return lbl_img

def open_text(frame, name, points):
    lbl_text = tk.Label(frame, text=f'{name} with {points} points')
    lbl_text.configure(background=COLOR, foreground=TEXT_COLOR)

    return lbl_text

def clear(root):
    for ele in root.winfo_children():
        if not isinstance(ele, tk.Button):
            ele.destroy()

def main(root):
    root.configure(background=COLOR)
    root.geometry("600x600")
    #root.geometry("1920x1080")
    root.resizable(False, False)
    
    tk.Button(root, text="Add",command=lambda: addfile(root)).grid(sticky="we")
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    main(root)