import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinterdnd2 import *
from PIL import Image, ImageTk
import csv
import os
from pathlib import Path
import requests
import shutil
from packaging import version as vs
import sys

import tkinterdnd2

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


def addfile(event, root):
    global data
    file = event.data
    _, ext = os.path.splitext(file)
    if (not file) or (ext != ".csv"):
        create_error("Please use a valid file.")
        return

    with open(file, mode="r", encoding="utf-8-sig") as c:
        reader = csv.DictReader(c)
        check = True if data else False
        for row in reader:
            row = {k.strip():v.strip() for k,v in row.items()}
            points = int(row.get("kill")) * kill_points + placement_points.get(row.get("rank"))

            
            if check:
                nickname = row.get("nickname")
                data[nickname]["points"] += points
                data[nickname]["row"].append(row)
            else:
                data[row.get("nickname")] = {
                                            "points": points,
                                            "row": [row],
                                            "manual": 0
                                            }
        
    create_frame(root)

def create_frame(root):
    global data
    clear(root)

    data = {k:v for k,v in sorted(data.items(), key=lambda item:item[1].get("points"), reverse=True)}
    counter, counter2 = 0, 0
    
    for k, v in data.items():
        if counter >= 9:
            counter, counter2 = 0, 1     
        insideFrame = tk.Frame(root)
        insideFrame.configure(background=COLOR, highlightbackground=TEXT_COLOR, highlightthickness=1)
        insideFrame.grid(sticky="w", row=counter, column=counter2, padx=50)

        column = 0
        for img in v.get("row"):
           open_img(insideFrame, img).grid(row=counter, column=column, columnspan=1, sticky="w")
           column += 1
        l = open_text(insideFrame, k)
        l.bind("<Button-1>", lambda event, x=root, y=k: increment(event, x, y))
        l.bind("<Button-3>", lambda event, x=root, y=k: decrement(event, x, y))
        l.grid(columnspan=len(v.get("row")))

        counter +=1


def increment(event, root, name):
    global data
    data[name]["points"] += 1
    data[name]["manual"] += 1
    create_frame(root)
    

def decrement(event, root, name):
    global data
    data[name]["points"] -= 1
    data[name]["manual"] -= 1
    create_frame(root)

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

def open_text(frame, name):
    lbl_text = tk.Label(frame, anchor="w", text=f'{name} with {data[name]["points"]} points\nManual points added: {data[name]["manual"]}')
    lbl_text.configure(background=COLOR, foreground=TEXT_COLOR)

    return lbl_text

def clear(root):
    for ele in root.winfo_children():
        if not isinstance(ele, tk.Button):
            ele.destroy()

def create_error(msg):
    messagebox.showerror("Error", msg)

def download_file():
    version = open('version.txt').read()
    url = f"https://github.com/HametAk/TournamentCalculator/releases/download/{version}/tourney.exe"
    local_filename = f"tourney_{version}.exe"
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def check_version():
    version_file = os.path.join(Path(__file__).parent, "version.txt")
    version = open(version_file).read()
    tag = requests.get("https://api.github.com/repos/HametAk/TournamentCalculator/releases/latest").json().get("tag_name")
    if not tag:
        return
    if vs.parse(version) < vs.parse(tag):
        if messagebox.askyesno("Update?", "Do you want to update this program? It is highly recommended."):
            download_file()
            with open("version.txt", "w") as v:
                v.write(tag)
            messagebox.showinfo("Press Ok to finish your installation.")
            sys.exit()

def main(root):
    root.configure(background=COLOR)
    root.geometry("700x700")
    root.resizable(False, False)

    f = tk.Frame(root, height=700, width=700, background=COLOR, highlightbackground=TEXT_COLOR)
    f.pack()
    f.drop_target_register(DND_FILES)
    f.dnd_bind('<<Drop>>', lambda event, x=f: addfile(event, x))
    
    #check for Updates
    check_version()

    root.mainloop()

if __name__ == "__main__":
    root = tkinterdnd2.Tk()
    main(root)