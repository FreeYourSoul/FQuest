# /bin/python

from os import listdir
from os.path import isfile, join

from tkinter.filedialog import *
import argparse
import json


class NpcConfig:

    def __init__(self, fileIO):
        self._name = "Name"
        self._id = 10
        self._worldServer = "WS00"
        self._luaScript = ""
        # Position relative to the WorldServer
        self._position_x = 0.0
        self._position_y = 0.0
        self._devNotes = ""
        self._npcRelations = {}
        self._isMerchant = False


class FQuest:

    def __init__(self, pathToNpcFolder):
        self._pathToNpcFolder = pathToNpcFolder
        self._window = Tk()
        self._firstFrame = Frame(self._window, borderwidth=2, relief=GROOVE)
        searchFrame = Frame(self._firstFrame).pack()
        self._searchNPC = Entry(searchFrame, width=30).pack(side=LEFT)
        Button(searchFrame, text='Search', command=self.searchNPC).pack(side=RIGHT)
        self._firstFrame.pack(side=LEFT, padx=10, pady=10)
        self._listNpc = Listbox(self._firstFrame)
        self._listNpc.pack()
        self._listNpc.bind('<<ListboxSelect>>', self.onListNpcSelect)
        self._secondFrame = Frame(self._window, borderwidth=2, relief=GROOVE)
        self._secondFrame.pack(side=RIGHT, padx=10, pady=10)
        self.setupNpcListbox()
        self._searchNPC = StringVar()

        Label(self._firstFrame, text="Existing NPCs").pack(padx=10, pady=10)
        Button(self._firstFrame, text='Add NPC in list', command=self.retrieveNpcConfigInformations).pack()
        Label(self._secondFrame, text="Current NPC").pack(padx=10, pady=10)

    def searchNPC(self):
        try:
            index = self._listNpc.get(0, "end").index(self._searchNPC.get())
            self._listNpc.select_set(index)
        except ValueError:
            print("None npc found with name : ", self._searchNPC.get())

    def setupNpcListbox(self):
        print(os.listdir(self._pathToNpcFolder))
        for f in (f for f in listdir(self._pathToNpcFolder) if isfile(join(self._pathToNpcFolder, f))):
            splits = os.path.splitext(f)[0].split("_")
            print("File : ", splits)
            self._listNpc.insert(END, splits[1])

    def onListNpcSelect(self, evt):
        index = int(self._listNpc.curselection()[0])
        value = self._listNpc.get(index)
        print("NPC Selection : ", index, " - ", value)

    def retrieveNpcConfigInformations(self):
        filename = askopenfilename(title="Open config file", filetypes=[('config files', '.xml'), ('all files', '.*')])
        fichier = open(filename, "r")
        content = fichier.read()
        jsonLoaded = json.loads(content)
        fichier.close()

    def display(self):
        self._window.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc", help="path to the NPC folder")
    args = parser.parse_args()
    print("start FQuest with base path : ", args.npc)
    parser.parse_args()
    FQuest(args.npc).display()
