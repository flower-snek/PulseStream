import asyncio
import websockets
import json
from tkinter import *

f = open("basic_theme.json")
tj = json.load(f)
f.close()

window = Tk()
window.geometry("{}x{}".format(tj["width"], tj["height"]))

canvas = Canvas(window, width=tj["width"], height=tj["height"], background="#0000FF")
canvas.pack()


def round_rectangle(x1, y1, x2, y2, r=25,
                    **kwargs):  # thanks stack overflow https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners?rq=1
    points = (
    x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y1 + r, x2, y2 - r, x2, y2 - r, x2, y2,
    x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)


def parallelogram(x1, y1, x2, y2, off, vert=False, **kwargs):
    if off > 0:
        if not vert:
            points = (x1 + off, y1, x2, y1, x2 - off, y2, x1, y2)
        else:
            points = (x1, y1 + off, x2, y1, x2, y2 - off, x1, y2)
    else:
        if not vert:
            points = (x1, y1, x2 + off, y1, x2, y2, x1 - off, y2)
        else:
            points = (x1, y1, x2, y1 - off, x2, y2, x1, y2 + off)
    return canvas.create_polygon(points, **kwargs)


window.configure(background=tj["bg_color"])

window.wm_attributes("-topmost", True)
window.wm_attributes("-transparentcolor", tj["trans_color"])
stat_labels = []

JUDGE_COLORS = ["#A844DB", "#44A7E4", "#44EE44", "#EEAF44", "#D04444"]
API_GETS = ["hitStats", "hitStats", "hitStats", "hitStats", "hitStats",  # 0-4: Marv count, Good count, ..., Miss count
            "acc",  # 5: Accuracy
            "title",  # 6: Last played song title
            "stars",  # 7: Last played star count
            "mods",  # 8: Current list of mods
            "score",  # 9: Current score
            "playing",  # 10: Is the song currently playing?
            # (Note: the song stops playing before the start so this isn't the best indicator of if the player is mid-song or not but it's not the worst either, let me know if you find a better one)
            "sel_id"  # 11: Currently SELECTED song ID
            # (I couldn't find a way to get the currently playing song ID, or the currently selected song name - if you know a way, let me know!!!)
            ]

''' old """theme"""
for i in range(5):
    # stat_labels.append(Label(text="0", bg=colors[i], height=2, width=5, relief='flat', borderwidth=5, font=("Quicksand", 20, "bold")))
    # stat_labels[i].pack()
    round_rectangle(55 + 100*i, 5, 145+100*i, 95, 25, fill=colors[i])
    stat_labels.append(canvas.create_text(100 + 100*i, 50, text="loading", font=("Quicksand", 20, "bold")))
'''

# draw all objects in the theme json in order

for i in tj["items"]:
    if "type" in i:
        ty = i["type"]
        color = "#000000"
        if "color" in i:
            color = i["color"]
            if isinstance(color, int):
                color = JUDGE_COLORS[color]
        if ty == "box":
            if "r" in i:
                round_rectangle(i["x"], i["y"], i["x"] + i["w"], i["y"] + i["h"], i["r"], fill=color)
            else:
                canvas.create_rectangle(i["x"], i["y"], i["x"] + i["w"], i["y"] + i["h"], fill=color)
        if ty == "plg":
            if "vert" in i:
                parallelogram(i["x"], i["y"], i["x"] + i["w"], i["y"] + i["h"], i["off"], i["vert"], fill=color)
            else:
                parallelogram(i["x"], i["y"], i["x"] + i["w"], i["y"] + i["h"], i["off"], fill=color)
        if ty == "txt":
            just = "center"
            if "justify" in i:
                just = i["justify"]
            if isinstance(i["val"], str):
                # if its a string its an absolute value just print it no fuss
                canvas.create_text(i["x"], i["y"], text=i["val"], font=("Quicksand", i["size"], "bold"), fill=color,
                                   anchor=just)
            else:
                # if its a number its an api value, just put a dummy value in and wait for the update loop
                dummy = "Loading"
                if "ldval" in i:
                    dummy = i["ldval"]
                p = ""
                if "prefix" in i:
                    p = i["prefix"]
                s = ""
                if "suffix" in i:
                    s = i["suffix"]
                stat_labels.append((
                                   canvas.create_text(i["x"], i["y"], text=dummy, font=("Quicksand", i["size"], "bold"),
                                                      fill=color, anchor=just), i["val"], p, s))

#######################################################


close = False


async def echo(websocket):
    async for message in websocket:
        global close
        if close:
            return
        # print(data)
        try:
            data = json.loads(message)
            for j in stat_labels:
                data_id = j[1]
                # print(stat_labels[i])
                get_data = data[API_GETS[data_id]]

                if data_id < 5:  # Marv - Miss counters
                    get_data = get_data[data_id]

                # clean up data for printing
                if data_id == 5 or data_id == 7 or data_id == 9:  # Acc, Stars, Score
                    get_data = round(get_data, 2)
                if data_id == 8:  # Mods
                    mod_string = ""
                    if get_data["bpm"] != 1:
                        mod_string = "{}BPM {}x, ".format(mod_string, get_data["bpm"])
                    if get_data["foresight"] != 1:
                        mod_string = "{}FS {}x, ".format(mod_string, get_data["foresight"])
                    if get_data["hitWindow"] != 1:
                        mod_string = "{}HW {}x, ".format(mod_string, get_data["hitWindow"])
                    mod_string = "{}NF, ".format(mod_string) if get_data["noFail"] else mod_string
                    mod_string = "{}HD, ".format(mod_string) if get_data["hidden"] else mod_string
                    mod_string = "{}NE, ".format(mod_string) if get_data["noFail"] else mod_string
                    mod_string = "{}AT, ".format(mod_string) if get_data["auto"] else mod_string
                    mod_string = "{}IF, ".format(mod_string) if get_data["instantFail"] else mod_string
                    mod_string = "{}PF, ".format(mod_string) if get_data["perfect"] else mod_string
                    mod_string = "{}MR, ".format(mod_string) if get_data["mirror"] else mod_string
                    mod_string = "{}NR, ".format(mod_string) if get_data["noRelease"] else mod_string
                    mod_string = "{}RD, ".format(mod_string) if get_data["random"] else mod_string
                    mod_string = "{}FL, ".format(mod_string) if get_data["flashlight"] else mod_string
                    mod_string = mod_string.strip(", ")
                    # there was absolutely a better way to do this. no i'm not gonna do it.
                    # print("String", mod_string)

                    if mod_string == "":
                        mod_string = "No Mods"
                    get_data = mod_string

                canvas.itemconfigure(j[0], text="{}{}{}".format(j[2], get_data, j[3]))
        except:
            pass
        await websocket.send(message)


async def bg_tsk(flag):
    global close
    while not close:
        window.update()
        await asyncio.sleep(0.1)
    flag.set()


async def main():
    async with websockets.serve(echo, "localhost", 3757):
        flag = asyncio.Event()
        asyncio.create_task(bg_tsk(flag))
        await flag.wait()


def exit_loop():
    global close
    window.destroy()
    close = True


window.update()

# btn = Button(text='Close', bd='5', command=exit_loop)
# btn.pack()

window.protocol("WM_DELETE_WINDOW", exit_loop)

asyncio.run(main())
