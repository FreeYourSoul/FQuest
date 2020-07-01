# /bin/python

import argparse
import json
from os import listdir
from os.path import isfile, join
from tkinter import messagebox
from tkinter.filedialog import *


class NpcConfig:

    def __init__(self, fileIO):
        jsonLoaded = json.loads(fileIO.read())

        print("file : ", fileIO, "\njson :", jsonLoaded, "\n")

        # Position relative to the WorldServer
        self.name = jsonLoaded["name"]
        self.id = jsonLoaded["id"]
        self.worldServer = jsonLoaded["server"]
        self.luaScript = ""
        self.position_x = jsonLoaded["position_x"]
        self.position_y = jsonLoaded["position_y"]
        self.devNotes = jsonLoaded["lore"]
        self.npcRelations = {}
        self.isMerchant = False


class MapModule:
    _open = False

    def __init__(self):
        pass

    def close(self):
        self._open = False

    def display(self):
        if self._open is True:
            pass
        self._open = True
        root = Tk()

        def on_closing():
            if messagebox.askokcancel("Save and quit", "Do you want to quit?"):
                root.destroy()
                self._open = False

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()


class ScriptLuaModule:
    _open = False

    def __init__(self):
        pass

    def display(self):
        if self._open is True:
            pass
        self._open = True
        root = Tk()

        def on_closing():
            if messagebox.askokcancel("Save and quit", "Do you want to quit?"):
                root.destroy()
                self._open = False

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()


class FQuest:
    _mapIdxToId = {}

    def __init__(self, pathToNpcFolder):
        self._pathToNpcFolder = pathToNpcFolder
        self._window = Tk()

        self._mapModule = MapModule()
        self._scriptLUA = ScriptLuaModule()

        # First Frame :: Search Existing NPC
        self._firstFrame = PanedWindow(self._window, orient=VERTICAL)
        searchFrame = PanedWindow(self._firstFrame, orient=HORIZONTAL)
        searchFrame.pack()
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.setupNpcListbox())
        self._searchNPC = Entry(searchFrame, textvariable=sv, width=30)
        searchFrame.add(Label(searchFrame, text='Search by Id/Name : '))
        searchFrame.add(self._searchNPC)
        self._listNpc = []
        self._listNpcBox = Listbox(self._firstFrame)
        self._listNpcBox.bind('<<ListboxSelect>>', self.onListNpcSelect)
        self._firstFrame.add(Label(self._firstFrame, text="Existing NPCs", anchor=CENTER))
        self._firstFrame.add(self._listNpcBox)
        self._firstFrame.add(searchFrame)
        self._firstFrame.add(
            Button(self._firstFrame, text='Add NPC in list', command=lambda: self.updateLeftPanel(
                askopenfilename(title="Open npc file", filetypes=[('npc file', '.xml'), ('all', '.*')]))))
        self.setupNpcListbox()

        # Second Frame :: Update / Read current NPC Selection
        self._secondFrame = PanedWindow(self._window, orient=VERTICAL)

        firstLine = PanedWindow(self._window, orient=HORIZONTAL)
        secondLine = PanedWindow(self._window, orient=HORIZONTAL)
        thirdLine = PanedWindow(self._window, orient=HORIZONTAL)

        self._id = Entry(firstLine)
        self._currentSelectionName = Entry(firstLine)
        self._x = Entry(secondLine)
        self._y = Entry(secondLine)
        self._lore = Text(thirdLine, height=10)

        firstLine.add(Label(firstLine, text='Id : '))
        firstLine.add(self._id)
        firstLine.add(Label(firstLine, text='Name : '))
        firstLine.add(self._currentSelectionName)

        secondLine.add(Label(secondLine, text='Pos x : '))
        secondLine.add(self._x)
        secondLine.add(Label(secondLine, text='Pos y : '))
        secondLine.add(self._y)
        secondLine.add(Button(secondLine, text='Map'))

        thirdLine.add(Label(thirdLine, text='Lore : '))
        thirdLine.add(self._lore)

        self._secondFrame.add(Label(self._secondFrame, text="Current selected NPC"))
        self._secondFrame.add(firstLine)
        self._secondFrame.add(secondLine)
        self._secondFrame.add(Button(self._secondFrame, text='Lua Script', command=lambda: self._scriptLUA.display()))
        self._secondFrame.add(thirdLine)
        self._secondFrame.add(Button(self._secondFrame, text='Save'))

        self._firstFrame.pack(side=LEFT, expand=Y, fill=BOTH, pady=2, padx=2)
        self._secondFrame.pack(side=RIGHT, expand=Y, padx=10, pady=10)

    def setupNpcListbox(self):
        self._listNpc = []
        self._mapIdxToId = {}
        self._listNpcBox.delete(0, END)
        i = 0
        for f in (f for f in listdir(self._pathToNpcFolder) if isfile(join(self._pathToNpcFolder, f))):
            npcFullName = os.path.splitext(f)[0]
            self._listNpc.append(npcFullName)
            if self._searchNPC.get().upper() in npcFullName.upper():
                splits = npcFullName.split("_")
                self._mapIdxToId[i] = int(splits[0])
                self._listNpcBox.insert(END, splits[1])
                i += 1

    def updateLeftPanel(self, filePath):
        file = open(filePath, "r")

        cfg = NpcConfig(file)
        self._id.delete(0, END)
        self._currentSelectionName.delete(0, END)
        self._x.delete(0, END)
        self._y.delete(0, END)
        self._lore.delete('1.0', END)

        self._id.insert(0, cfg.id)
        self._currentSelectionName.insert(0, cfg.name)
        self._x.insert(0, cfg.position_x)
        self._y.insert(0, cfg.position_y)
        self._lore.insert(INSERT, cfg.devNotes)
        file.close()

    def onListNpcSelect(self, evt):
        index = int(self._listNpcBox.curselection()[0])
        self.setupNpcListbox()
        print("index : ", index)
        print("self._mapIdxToId[index] : ", self._mapIdxToId[index])
        print("NPC Selection : id_name: ", self._listNpc[int(self._mapIdxToId[index])], " => index:", index, ", value: ", self._listNpcBox.get(index))
        self.updateLeftPanel(self._pathToNpcFolder + "/" + self._listNpc[int(self._mapIdxToId[index])] + ".json")

    def display(self):
        self._window.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc", help="path to the NPC folder")
    args = parser.parse_args()

    print("start FQuest with base path : ", args.npc)
    parser.parse_args()
    FQuest(args.npc).display()
